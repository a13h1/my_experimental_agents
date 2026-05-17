#!/usr/bin/env python3
import argparse
import getpass
import json
import os
import sys

from openai import OpenAI


def get_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key

    try:
        api_key = getpass.getpass("Enter your OpenAI API key: ")
    except Exception:
        api_key = input("Enter your OpenAI API key: ")

    if not api_key:
        print("Error: OpenAI API key is required.")
        sys.exit(1)

    return api_key


def lookup_domain_info(domain: str) -> str:
    """Retrieve mock business information for a domain."""
    print(f"-> TOOL ACTIVATED: lookup_domain_info(domain={domain})")

    mock_data = {
        "acmecorp.com": {
            "industry": "Software/SaaS",
            "size": "501-1000 employees",
            "revenue": "$50M - $100M",
        },
        "widgetco.net": {
            "industry": "Manufacturing",
            "size": "100-250 employees",
            "revenue": "$10M - $25M",
        },
        "globalfin.org": {
            "industry": "Financial Services",
            "size": "5000+ employees",
            "revenue": "$1B+",
        },
    }

    info = mock_data.get(domain, {"industry": "Unknown", "size": "N/A", "revenue": "N/A"})
    return json.dumps(info)


def check_crm_history(email: str) -> str:
    """Return mock CRM contact history for an email address."""
    print(f"-> TOOL ACTIVATED: check_crm_history(email={email})")

    mock_data = {
        "jane@acmecorp.com": {
            "last_contact": "2025-11-15",
            "status": "Cold Lead",
            "notes": "Attended webinar, no follow-up yet.",
        },
        "bob@widgetco.net": {
            "last_contact": "2025-12-01",
            "status": "Active Opportunity",
            "notes": "Discussed Q1 budget and product integration.",
        },
    }

    history = mock_data.get(email.lower(), {"last_contact": "N/A", "status": "No Record", "notes": "New lead, first contact opportunity."})
    return json.dumps(history)


def calculate_lead_score(data_summary: str) -> str:
    """Score the lead based on collected domain and CRM information."""
    print("-> TOOL ACTIVATED: calculate_lead_score(...)" )

    data = json.loads(data_summary)
    domain_info = data.get("domain_info", {})
    crm_history = data.get("crm_history", {})

    score = "Low"
    revenue = domain_info.get("revenue", "")
    status = crm_history.get("status", "")

    if revenue.startswith("$1B+"):
        score = "High"
    elif status == "Active Opportunity":
        score = "High"
    elif revenue.startswith("$50M"):
        score = "Medium"
    elif status == "Cold Lead":
        score = "Medium"

    return json.dumps({"lead_score": score})


AVAILABLE_FUNCTIONS = {
    "lookup_domain_info": lookup_domain_info,
    "check_crm_history": check_crm_history,
    "calculate_lead_score": calculate_lead_score,
}

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "lookup_domain_info",
            "description": "Retrieve business information about a company based on its domain.",
            "parameters": {
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "Company domain name, e.g. acmecorp.com."},
                },
                "required": ["domain"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_crm_history",
            "description": "Look up CRM contact history for a lead email address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Full lead email address."},
                },
                "required": ["email"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_lead_score",
            "description": "Assign a High/Medium/Low lead score based on the combined lead data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data_summary": {"type": "string", "description": "JSON string containing domain_info and crm_history."},
                },
                "required": ["data_summary"],
            },
        },
    },
]


def run_agent(client: OpenAI, user_prompt: str) -> str:
    system_prompt = (
        "You are an expert CRM Lead Qualifier Agent. Your task is to qualify a sales lead based on an email address. "
        "Follow these steps exactly: 1) extract the domain from the email, 2) call lookup_domain_info, "
        "3) call check_crm_history, 4) combine the collected data, 5) call calculate_lead_score, "
        "and 6) provide a concise summary of the findings and final recommendation."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    collected_data = {}

    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=TOOLS_SCHEMA,
            tool_choice="auto",
        )

        response_message = response.choices[0].message
        messages.append(response_message)

        tool_calls = getattr(response_message, "tool_calls", None)
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                tool_func = AVAILABLE_FUNCTIONS.get(function_name)

                if not tool_func:
                    raise RuntimeError(f"Unknown tool requested: {function_name}")

                if function_name == "calculate_lead_score":
                    function_args = {"data_summary": json.dumps(collected_data)}

                tool_result = tool_func(**function_args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": tool_result,
                })

                if function_name == "lookup_domain_info":
                    collected_data["domain_info"] = json.loads(tool_result)
                elif function_name == "check_crm_history":
                    collected_data["crm_history"] = json.loads(tool_result)
                elif function_name == "calculate_lead_score":
                    collected_data["lead_score"] = json.loads(tool_result).get("lead_score")

            continue

        return response_message.content


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="CRM Lead Qualifier Agent - standalone Python application"
    )
    parser.add_argument(
        "email",
        nargs="?",
        help="Lead email address to qualify, e.g. jane@acmecorp.com",
    )
    parser.add_argument(
        "--prompt",
        default="Please qualify this lead and summarize all findings.",
        help="Optional prompt to customize the agent request.",
    )
    parser.add_argument(
        "--api-key",
        help="OpenAI API key. Otherwise reads from OPENAI_API_KEY environment variable.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    api_key = args.api_key or get_api_key()
    os.environ["OPENAI_API_KEY"] = api_key

    if not args.email:
        args.email = input("Enter the lead email address: ").strip()

    if not args.email:
        print("Error: Lead email address is required.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    user_prompt = f"{args.prompt} The lead email is: {args.email}"

    try:
        summary = run_agent(client, user_prompt)
        print("\n=== Lead Qualification Summary ===\n")
        print(summary)
        print("\n=== End of Summary ===")
    except Exception as exc:
        print(f"Error running agent: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
