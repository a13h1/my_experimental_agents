import streamlit as st
import pandas as pd
import os
import json
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from typing import List, Optional
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="Hello Agent - Multi-Agent Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🤖 Hello Agent - Multi-Agent Platform")
st.markdown("""
An integrated platform with multiple AI agents:
- **CSV FAQ Agent**: Upload and query CSV data with natural language
- **CRM Lead Qualifier**: Qualify sales leads using domain and CRM data
""")

# ========================
# CRM Agent Functions
# ========================

def get_available_api_key() -> str:
    """Get OpenAI API key from environment or sidebar input."""
    return os.environ.get("OPENAI_API_KEY", "")


def lookup_domain_info(domain: str) -> str:
    """Retrieve mock business information for a domain."""
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
    try:
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
    except Exception as e:
        return json.dumps({"lead_score": "Error", "error": str(e)})


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


def run_crm_agent(client: OpenAI, user_prompt: str) -> str:
    """Run the CRM lead qualifier agent."""
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

# Sidebar for API key configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input(
        "Enter your OpenAI API Key",
        type="password",
        help="Your API key is not stored. It's only used for this session."
    )
    
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.success("✓ API Key configured")
    else:
        st.warning("⚠️ Please enter your OpenAI API Key to proceed")

# Main content area
if api_key:
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Preview", "❓ Ask Questions", "🎯 CRM Lead Qualifier"])
    
    with tab1:
        st.subheader("Step 1: Upload CSV Files")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Choose CSV file(s)",
            type=["csv"],
            accept_multiple_files=True,
            help="You can upload multiple CSV files at once"
        )
        
        if uploaded_files:
            st.success(f"✓ {len(uploaded_files)} file(s) uploaded")
            
            # Store uploaded dataframes in session state
            if "dataframes" not in st.session_state:
                st.session_state.dataframes = {}
            if "file_names" not in st.session_state:
                st.session_state.file_names = []
            
            # Load and display each file
            st.subheader("📊 Data Preview")
            
            for uploaded_file in uploaded_files:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.session_state.dataframes[uploaded_file.name] = df
                    if uploaded_file.name not in st.session_state.file_names:
                        st.session_state.file_names.append(uploaded_file.name)
                    
                    # Display file info and preview
                    with st.expander(f"📄 {uploaded_file.name}", expanded=False):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Rows", len(df))
                        with col2:
                            st.metric("Columns", len(df.columns))
                        with col3:
                            st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
                        
                        st.write("**Column Names:**")
                        st.write(", ".join(df.columns.tolist()))
                        
                        st.write("**First few rows:**")
                        st.dataframe(df.head(), use_container_width=True)
                        
                except Exception as e:
                    st.error(f"Error reading {uploaded_file.name}: {str(e)}")
        else:
            st.info("👆 Upload CSV files to get started")
    
    with tab2:
        st.subheader("Step 2: Ask Your Question")
        
        if "dataframes" not in st.session_state or not st.session_state.dataframes:
            st.warning("Please upload CSV files first using the 'Upload & Preview' tab")
        else:
            st.info(f"📚 Loaded {len(st.session_state.dataframes)} file(s): {', '.join(st.session_state.file_names)}")
            
            # System prompt for data-only responses
            system_prompt = """
You are a helpful data assistant that answers questions based ONLY on the provided CSV data.

IMPORTANT RULES:
1. You MUST only use information from the uploaded CSV files
2. Do NOT use any general knowledge or information outside the data
3. If the answer is not in the data, clearly state: "I could not find this information in the uploaded files"
4. When answering, be specific and quote relevant data from the tables
5. If a question is ambiguous, ask for clarification based on the data structure
6. Always be honest about what information is or is not available

Your goal is to help users find answers in their data quickly and accurately.
"""
            
            # Question input
            user_question = st.text_area(
                "What would you like to know?",
                placeholder="E.g., 'What is the return policy for electronics?' or 'What are the API rate limits?'",
                height=100
            )
            
            # Submit button
            if st.button("🔍 Search for Answer", type="primary"):
                if not user_question.strip():
                    st.error("Please enter a question")
                else:
                    with st.spinner("🤔 AI is thinking..."):
                        try:
                            # Initialize LLM
                            llm = ChatOpenAI(
                                model="gpt-4o-mini",
                                temperature=0.0,
                                api_key=api_key
                            )
                            
                            # Prepare dataframes list
                            dataframes_list = list(st.session_state.dataframes.values())
                            
                            # Create agent
                            agent = create_pandas_dataframe_agent(
                                llm,
                                dataframes_list,
                                verbose=False,
                                agent_type="openai-functions",
                                allow_dangerous_code=True
                            )
                            
                            # Combine system prompt with user question
                            final_query = f"{system_prompt}\n\nQuestion: {user_question}"
                            
                            # Get answer
                            result = agent.invoke(final_query)
                            response = result.get('output', 'No response generated')
                            
                            # Display answer
                            st.success("✓ Answer Found")
                            st.markdown("### Answer:")
                            st.write(response)
                            
                            # Add to chat history
                            if "chat_history" not in st.session_state:
                                st.session_state.chat_history = []
                            
                            st.session_state.chat_history.append({
                                "question": user_question,
                                "answer": response
                            })
                            
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            
            # Display chat history
            if "chat_history" in st.session_state and st.session_state.chat_history:
                st.divider()
                st.subheader("📋 Question History")
                
                for i, item in enumerate(reversed(st.session_state.chat_history[-5:]), 1):
                    with st.expander(f"Q{len(st.session_state.chat_history) - i}: {item['question'][:50]}..."):
                        st.write("**Question:**", item['question'])
                        st.write("**Answer:**", item['answer'])
    
    with tab3:
        st.subheader("🎯 CRM Lead Qualifier Agent")
        st.markdown("""
Qualify sales leads by analyzing company information and CRM history.
Enter a lead email address and the agent will:
1. Extract the company domain
2. Look up company information
3. Check CRM contact history
4. Calculate a lead score (High/Medium/Low)
5. Provide a qualification summary
        """)
        
        # Lead email input
        lead_email = st.text_input(
            "Enter lead email address",
            placeholder="e.g., jane@acmecorp.com",
            help="The email address of the sales lead to qualify"
        )
        
        # Custom prompt (optional)
        custom_prompt = st.text_area(
            "Custom instructions (optional)",
            placeholder="E.g., 'Focus on revenue potential' or 'Check if they are in our target industry'",
            height=60
        )
        
        # Qualify button
        if st.button("🔍 Qualify Lead", type="primary", key="qualify_lead"):
            if not lead_email.strip():
                st.error("Please enter a lead email address")
            elif not api_key:
                st.error("API key not configured. Please enter your OpenAI API Key in the sidebar.")
            else:
                with st.spinner("🤔 Analyzing lead..."):
                    try:
                        client = OpenAI(api_key=api_key)
                        
                        # Build the prompt
                        base_prompt = f"Please qualify this lead and summarize all findings. The lead email is: {lead_email}"
                        if custom_prompt.strip():
                            base_prompt += f"\n\nAdditional instructions: {custom_prompt}"
                        
                        # Run the agent
                        result = run_crm_agent(client, base_prompt)
                        
                        # Display result
                        st.success("✓ Lead Qualification Complete")
                        st.markdown("### Lead Qualification Summary:")
                        st.write(result)
                        
                        # Store in session history
                        if "crm_history" not in st.session_state:
                            st.session_state.crm_history = []
                        
                        st.session_state.crm_history.append({
                            "email": lead_email,
                            "summary": result,
                        })
                        
                    except Exception as e:
                        st.error(f"❌ Error qualifying lead: {str(e)}")
        
        # Display qualification history
        if "crm_history" in st.session_state and st.session_state.crm_history:
            st.divider()
            st.subheader("📋 Lead Qualification History")
            
            for i, item in enumerate(reversed(st.session_state.crm_history[-5:]), 1):
                with st.expander(f"Lead {len(st.session_state.crm_history) - i}: {item['email']}"):
                    st.write("**Summary:**")
                    st.write(item['summary'])
else:
    st.error("🔐 Please enter your OpenAI API Key in the sidebar to continue")
