import streamlit as st
import pandas as pd
import os
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from typing import List, Optional

# Page configuration
st.set_page_config(
    page_title="Hello Agent - CSV FAQ Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🤖 Hello Agent - CSV FAQ Agent")
st.markdown("""
This tool lets you upload CSV files and ask natural language questions about the data.
The AI will search through your files and provide answers based on the actual data.
""")

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
    tab1, tab2 = st.tabs(["📤 Upload & Preview", "❓ Ask Questions"])
    
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
else:
    st.error("🔐 Please enter your OpenAI API Key in the sidebar to continue")
