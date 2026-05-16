# Hello Agent - CSV FAQ Agent 🤖

A Streamlit-based web application that uses AI to answer questions from CSV data. Perfect for support agents, product managers, and operations staff who need quick answers from documentation and FAQ files.

## Features ✨

- 📤 **Upload multiple CSV files** with instant preview
- ❓ **Ask natural language questions** about your data
- 🧠 **AI-powered answers** using LangChain and OpenAI
- 📊 **Data-only responses** - no general knowledge, only real data
- 🎯 **Clean, intuitive interface** built with Streamlit
- 💾 **Chat history** to review previous questions and answers

## Prerequisites

- Python 3.9+
- OpenAI API key
- pip (Python package manager)

## Installation

### 1. Clone or Download the Project

```bash
cd /Users/abhishek/projects/HelloAgent
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Setup

### 1. Get Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api/keys)
2. Create a new API key
3. Copy the key (you'll need it to run the app)

### 2. Prepare Your CSV Files

Place your CSV files in the `Datasets/` folder or have them ready to upload through the app.

Sample columns to include:
- **For FAQ files**: `question`, `answer`, or `topic`, `response`
- **For policies**: `policy_name`, `policy_details`, `effective_date`
- **For product docs**: `feature`, `description`, `limits`

## Running the App

### Start the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### First Time Use

1. **Enter your OpenAI API Key** in the sidebar (it's not stored, only used for your session)
2. **Upload CSV files** using the upload widget
3. **Preview your data** to verify it loaded correctly
4. **Ask questions** in the "Ask Questions" tab
5. **Review answers** - they're based only on your data

## Example Questions

For different data types, try these patterns:

**E-commerce FAQs:**
- "What is the return policy for electronics?"
- "How long do you offer extended warranty?"
- "What are the shipping costs?"

**Credit Card Terms:**
- "What is the APR for the basic card?"
- "Are there annual fees?"
- "What are the spending rewards?"

**Hospital Policies:**
- "What are the visiting hours?"
- "How do I request medical records?"
- "What is the payment policy?"

**SaaS Documentation:**
- "What is the API rate limit for the free plan?"
- "How many users can I add?"
- "What integrations are supported?"

## Project Structure

```
HelloAgent/
├── app.py                          # Main Streamlit application
├── hello_agent_csv_faq.py         # Original CLI version (reference)
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── Datasets/                       # Sample CSV files
│   ├── credit_card_terms.csv
│   ├── ecommerce_faqs.csv
│   ├── hospital_policy.csv
│   └── saas_docs.csv
├── Spec/                           # Project specifications
│   └── Question_Week 0 Mini Project.pdf
└── README.md                       # This file
```

## How It Works

### Architecture

1. **User uploads CSV files** → Converted to Pandas DataFrames
2. **User asks a question** → Combined with data-only system prompt
3. **LangChain agent processes** → Uses OpenAI to understand the question
4. **Agent queries DataFrames** → Searches through the data
5. **AI generates answer** → Based only on actual data found
6. **Answer displayed** → Ready to copy/paste

### System Prompt

The app uses a strict system prompt that ensures:
- Answers come ONLY from the data
- No speculation or general knowledge
- Clear responses when data isn't available
- Specific citations from the tables

## Key Settings

### Model Configuration

- **Model**: `gpt-4o-mini` (fast, cost-effective)
- **Temperature**: `0.0` (deterministic, no creativity)
- **Agent Type**: `openai-functions` (structured reasoning)

### Customization

To modify behavior, edit `app.py`:

```python
# Line ~160: Change the system prompt
system_prompt = """Your custom prompt here..."""

# Line ~198: Change the model
llm = ChatOpenAI(
    model="gpt-4o-mini",  # Or "gpt-4", "gpt-3.5-turbo"
    temperature=0.0,
    api_key=api_key
)
```

## Troubleshooting

### "API Key error"
- Check your OpenAI API key is correct
- Ensure your account has credits
- Verify API access is not restricted

### "No response" or Empty answer
- Check CSV format (must be valid CSV)
- Verify column names are clear
- Try rephrasing the question
- Check that data actually exists in the file

### "I could not find this information"
- The data might not be in the file
- Check the data with the preview tab
- Try different keywords
- Ensure case-sensitive matches when needed

### Slow responses
- Reduce the number of rows in your CSVs
- Ask more specific questions
- Check OpenAI API status

## Tips for Best Results

1. **Clean CSV files**: Remove empty rows and fix missing values
2. **Clear column names**: Use descriptive, single-line headers
3. **Consistent formatting**: Keep data types consistent (e.g., all dates same format)
4. **Good descriptions**: More detailed data = better answers
5. **Specific questions**: "What is the return policy?" vs "Tell me about returns"

## API Costs

This app uses the OpenAI API, which has associated costs:
- **gpt-4o-mini**: ~$0.00015 per 1K input tokens, $0.0006 per 1K output tokens
- Each question typically costs $0.001-$0.005
- The first file search is most expensive (includes full data context)

Monitor your usage at [OpenAI Usage](https://platform.openai.com/account/usage/overview)

## Features for Production

For a production version, consider:

- [ ] User authentication
- [ ] Database storage for chat history
- [ ] Rate limiting and quotas
- [ ] Caching for frequently asked questions
- [ ] Analytics on question patterns
- [ ] Support for more file formats (Excel, JSON, etc.)
- [ ] Vector embeddings for semantic search
- [ ] Feedback system for answer quality

## Security

- 🔐 API keys are **never stored**
- 💾 Chat history is **session-only** (lost on refresh)
- 📤 Files are **processed in memory** (not stored permanently)
- ✅ Always use environment variables for production

## Learning Resources

To understand how this works:

1. **Streamlit**: [Streamlit Docs](https://docs.streamlit.io)
2. **LangChain**: [LangChain Documentation](https://python.langchain.com)
3. **Pandas**: [Pandas Getting Started](https://pandas.pydata.org/docs/getting_started/index.html)
4. **OpenAI API**: [API Reference](https://platform.openai.com/docs/api-reference)

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review your CSV file format
3. Test with the sample data in `Datasets/` folder
4. Check OpenAI API status and limits

## License

This is an educational project. Feel free to modify and use as needed.

---

**Happy questioning! 🚀**
