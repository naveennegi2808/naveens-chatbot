import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import time
import google.generativeai as genai

# Load environment variables
load_dotenv()

# --- Critical Debugging for API Key ---
google_api_key = os.getenv('GOOGLE_API_KEY')
if not google_api_key:
    st.error("FATAL ERROR: GOOGLE_API_KEY environment variable not found.")
    st.info("Please ensure your .env file is correctly configured and located in the project root.")
    st.stop() # Stop the app if key is missing
else:
    # Configure the Google Generative AI SDK with the loaded key
    genai.configure(api_key=google_api_key)
# --- End Debugging ---


# Set page config for better appearance
st.set_page_config(
    page_title="Naveen's AI Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for main page content (excluding the floating chat, which is removed)
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .main-content {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .hero-section {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history and the LLM
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'model' not in st.session_state:
    # Initialize the LLM once and store it in session state
    st.session_state.model = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0.7)


# --- Main page content ---
st.markdown("""
<div class="main-content">
    <div class="hero-section">
        <h1>🤖 Welcome to Naveen's AI Assistant</h1>
        <p style="font-size: 1.2rem; margin-bottom: 0;">Powered by Google Gemini 2.5 Flash</p>
        <p>Start a conversation below!</p>
    </div>
</div>
""", unsafe_allow_html=True)


st.header("Chat with AI")

# Display chat messages from history on app rerun
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare chat history for LLM (just content, as Gemini expects strings or BaseMessage objects)
    # The `chathistory` list in your previous example was a list of strings,
    # so we'll keep that format for simplicity with the current model invoke.
    llm_history = [msg["content"] for msg in st.session_state.chat_history]

    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            try:
                # Invoke the Gemini model with the full conversation history
                # Note: `ChatGoogleGenerativeAI` expects a list of messages or a single string.
                # If sending full history, it's best to format as a list of strings for simple invoke.
                full_response = st.session_state.model.invoke(llm_history)
                response_content = full_response.content
            except Exception as e:
                response_content = f"An error occurred: {e}. Please check your API key, model availability, or quota."
            
            st.markdown(response_content)
    
    # Add assistant response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response_content})


# Footer
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem; margin-top: 3rem;">
    <small>Functional AI Chatbot</small>
</div>
""", unsafe_allow_html=True)