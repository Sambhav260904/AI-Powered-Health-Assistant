import streamlit as st

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    if "history" not in st.session_state:
        st.session_state.history = []

    if "last_summary" not in st.session_state:
        st.session_state.last_summary = None

    if "interaction_count" not in st.session_state:
        st.session_state.interaction_count = 0

    if "question_asked" not in st.session_state:
        st.session_state.question_asked = False

    if "summaries" not in st.session_state:
        st.session_state.summaries = {}
