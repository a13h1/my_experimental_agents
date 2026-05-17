# Multi-Agent Integration Guide

The **Hello Agent** platform now integrates two powerful AI agents in a single Streamlit application:

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Virtual environment (`.venv`) with dependencies installed
- OpenAI API key

### Run the App

```bash
cd /Users/abhishek/projects/HelloAgent
source .venv/bin/activate
streamlit run hello_agent_csv_faq.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📋 Available Agents

### Tab 1: 📤 Upload & Preview (CSV FAQ Agent)

**Purpose**: Query CSV data using natural language

**How to use**:
1. Go to the **Upload & Preview** tab
2. Click "Choose CSV file(s)" and upload one or more CSV files
3. Review the data preview (row/column counts, first rows)
4. Go to the **Ask Questions** tab

### Tab 2: ❓ Ask Questions (CSV FAQ Agent)

**Purpose**: Ask questions about your uploaded CSV data

**How to use**:
1. Make sure you've uploaded CSV files in Tab 1
2. Type your question (e.g., "What are the top 5 items by revenue?")
3. Click "🔍 Search for Answer"
4. View the AI's response based on your data
5. Previous questions appear in the Question History section

**Example Questions**:
- "What is the return policy for electronics?"
- "How many customers are in the US?"
- "What is the average order value?"

---

### Tab 3: 🎯 CRM Lead Qualifier

**Purpose**: Qualify sales leads by analyzing company data and CRM history

**How to use**:
1. Go to the **CRM Lead Qualifier** tab
2. Enter a lead email address (e.g., `jane@acmecorp.com`)
3. (Optional) Add custom instructions for focus areas
4. Click "🔍 Qualify Lead"
5. View the lead score and qualification summary
6. Check the Lead Qualification History for previous leads

**What the agent does**:
1. Extracts the company domain from the email
2. Looks up company business information (industry, size, revenue)
3. Checks CRM contact history and status
4. Calculates a lead score (High/Medium/Low)
5. Provides a summary with qualification reasoning and recommendation

**Example Leads**:
- `jane@acmecorp.com` - Software company, cold lead
- `bob@widgetco.net` - Manufacturing, active opportunity
- `any@company.com` - Unknown domain (will be treated as new lead)

**Custom Instructions Examples**:
- "Focus on revenue potential"
- "Check if they are in our target industry"
- "Consider this is a technical buyer"

---

## 🔑 Configuration

### API Key Setup

1. **In the Sidebar**: Enter your OpenAI API key in the text field
2. **Verification**: You'll see a "✓ API Key configured" message
3. **Environment Variable** (optional):
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   streamlit run hello_agent_csv_faq.py
   ```

---

## 🏗️ Architecture

### File Structure

```
/Users/abhishek/projects/HelloAgent/
├── hello_agent_csv_faq.py           # Main Streamlit app (all agents)
├── crm_lead_qualifier_agent.py      # Standalone CRM agent CLI
├── Datasets/                        # Sample CSV data
│   ├── credit_card_terms.csv
│   ├── ecommerce_faqs.csv
│   ├── hospital_policy.csv
│   └── saas_docs.csv
├── .streamlit/
│   └── config.toml
├── requirements.txt
└── README.md
```

### Agent Components

**CSV FAQ Agent (LangChain)**:
- Uses `ChatOpenAI` with `gpt-4o-mini` model
- Creates a `PandasDataFrameAgent` for dynamic data analysis
- System prompt enforces data-only responses
- Supports multiple CSV files

**CRM Lead Qualifier (OpenAI Functions)**:
- Uses OpenAI's function-calling API
- Tools: `lookup_domain_info`, `check_crm_history`, `calculate_lead_score`
- Agentic loop continues until no more tools are called
- Returns structured lead qualification summary

---

## 🛠️ Standalone Usage

You can also run the CRM Lead Qualifier as a standalone CLI app:

```bash
# With interactive prompt
.venv/bin/python crm_lead_qualifier_agent.py

# With email argument
.venv/bin/python crm_lead_qualifier_agent.py jane@acmecorp.com

# With custom API key
OPENAI_API_KEY="..." .venv/bin/python crm_lead_qualifier_agent.py bob@widgetco.net --prompt "Focus on revenue"
```

---

## 📊 Data Flow

```
User Input (Email/Question)
    ↓
[Tab 3: CRM Lead Qualifier] OR [Tab 2: CSV FAQ]
    ↓
OpenAI Function Calling / LangChain Agent
    ↓
Tool Calls (lookup_domain_info, check_crm_history, df.query, etc.)
    ↓
AI Processing & Response Generation
    ↓
Display Result → Add to History
```

---

## ⚙️ Models

- **CSV FAQ Agent**: `gpt-4o-mini` (faster, cost-effective)
- **CRM Lead Qualifier**: `gpt-4o` (more capable function calling)

Both models support function calling and are production-ready.

---

## 🐛 Troubleshooting

### "Error: Import tabulate failed"
- **Fix**: Run `pip install tabulate`
- Already included in `requirements.txt`

### API Key not working
- **Check**: Verify your OpenAI API key is valid
- **Scope**: Ensure your key has access to `gpt-4o` and `gpt-4o-mini`
- **Rate limits**: Check your API usage/quotas

### CSV Agent not finding columns
- **Check**: Ensure your CSV has proper headers
- **Debug**: Use the Preview tab to verify column names
- **Ask differently**: Reformulate your question to match column names

---

## 📝 Session State

Both agents maintain session history:
- **CSV FAQ**: Question history stored in `st.session_state.chat_history`
- **CRM Lead Qualifier**: Lead qualification history in `st.session_state.crm_history`

History persists during the session and resets on page refresh.

---

## 🔐 Security Notes

- API keys are **not stored** to disk
- Keys are only used for the active session
- History is stored in session state only (not persisted)
- CSV data is processed in memory (not sent to external systems beyond OpenAI)

---

## 📚 Next Steps

- Modify tool data in `AVAILABLE_FUNCTIONS` to connect to real CRM systems
- Add persistent history with a database backend
- Create custom system prompts for specific business use cases
- Integrate with Slack/Teams for team collaboration
- Add monitoring and logging for production use

