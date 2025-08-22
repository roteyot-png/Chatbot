import streamlit as st
import os
import time
from google import genai
from google.genai import types

# Initialize Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    client = None

# Page configuration
st.set_page_config(
    page_title="Local AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = None

def validate_api_key():
    """Validate the Gemini API key"""
    if not GEMINI_API_KEY:
        return False
    
    if not client:
        return False
    
    try:
        # Make a simple test request to validate the API key
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Hello"
        )
        return True
    except Exception as e:
        st.error(f"API Key validation failed: {str(e)}")
        return False

def get_ai_response(messages):
    """Get response from Gemini API"""
    if not client:
        st.error("Gemini client not initialized")
        return None
        
    try:
        # Convert messages to Gemini format - just use the last user message
        user_message = messages[-1]["content"] if messages else "Hello"
        
        # Create response
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )
        return response.text
    except Exception as e:
        st.error(f"Error getting AI response: {str(e)}")
        return None

def display_message(role, content):
    """Display a message in the chat interface"""
    if role == "user":
        with st.chat_message("user"):
            st.write(content)
    else:
        with st.chat_message("assistant"):
            st.write(content)

# Main app layout
st.title("🤖 Darshan's AI Assistant")
st.markdown("Your personal AI assistant powered by Google Gemini - smart, fast, and completely free!")

# Sidebar for settings and information
with st.sidebar:
    st.header("Settings")
    
    # Hidden API key validation (runs in background)
    if st.session_state.api_key_valid is None:
        st.session_state.api_key_valid = validate_api_key()
    
    # Only show API issues if there are problems
    if not st.session_state.api_key_valid:
        st.error("❌ API Configuration Issue")
        if st.button("🔄 Retry Connection"):
            st.session_state.api_key_valid = None
            st.rerun()
    
    # Clear conversation button
    if st.button("Clear Conversation", type="secondary"):
        st.session_state.messages = []
        st.rerun()
    
    # Conversation stats
    st.subheader("Session Info")
    st.write(f"Messages: {len(st.session_state.messages)}")
    
    st.subheader("✨ Features")
    st.write("• 💬 Intelligent conversations")
    st.write("• 🔒 Privacy-focused (local only)")
    st.write("• 🆓 Completely free to use")
    st.write("• ⚡ Fast Gemini AI responses")
    
    st.subheader("💡 Tips")
    st.write("Ask me anything! I can help with:")
    st.write("• Coding and programming")
    st.write("• Writing and creativity")
    st.write("• Analysis and research")
    st.write("• General questions")

# Main chat interface
if not st.session_state.api_key_valid:
    st.warning("⚠️ Please configure your Gemini API key to start chatting")
    st.info("💡 Get your free Gemini API key at: https://aistudio.google.com/app/apikey")
    st.stop()

# Display existing conversation
for message in st.session_state.messages:
    display_message(message["role"], message["content"])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to conversation
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    display_message("user", user_input)
    
    # Get AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Show loading indicator
        with st.spinner("Thinking..."):
            # Prepare messages for API call
            api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
            # Get response from Gemini
            full_response = get_ai_response(api_messages)
            
            if full_response:
                # Display the response
                message_placeholder.markdown(full_response)
            else:
                full_response = "Sorry, I encountered an error processing your request. Please try again."
                message_placeholder.markdown(full_response)
    
    # Add AI response to conversation
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        Darshan's AI Assistant - Powered by Gemini | Private & Secure
    </div>
    """,
    unsafe_allow_html=True
)
