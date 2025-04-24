import streamlit as st
import os
import datetime
from utils import initialize_session_state
from agent import (
    summarize_health_article,
    answer_health_question,
    generate_health_tips,
    check_api_key
)

# App title and description
st.set_page_config(
    page_title="Gemini-Powered Health Assistant",
    page_icon="🩺",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Sidebar for API key
with st.sidebar:
    st.title("🩺 Health Assistant")

    api_key = st.text_input(
        "Enter your Gemini API Key",
        type="password",
        value=st.session_state.get("api_key", os.getenv("GEMINI_API_KEY", "")),
        help="Get your API key from https://ai.google.dev/"
    )

    if api_key:
        st.session_state.api_key = api_key
        api_status = check_api_key(api_key)
        if api_status:
            st.success("API Key is valid!")
        else:
            st.error("Invalid API Key. Please check and try again.")

    st.markdown("---")
    st.markdown("""
    ### About
    This AI assistant helps with:
    - Summarizing health articles
    - Answering general health questions
    - Providing personalized wellness tips

    Powered by Google's Gemini API.
    """)

# Main content
st.title("Gemini-Powered Health Assistant")
st.markdown("Your AI companion for health insights, summaries, and tips.")

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["📰 Summarize Article", "🩺 Ask a Question", "💡 Get Wellness Tips"])

# Summarize Health Article tab
with tab1:
    st.header("Summarize a Health Article")
    st.markdown("Paste any health-related article or text to get a concise summary.")

    article_text = st.text_area(
        "Health Article Text",
        height=200,
        placeholder="Paste your health article or paragraph here...",
        key="article_input"
    )

    if st.button("Summarize Article", use_container_width=True):
        if not st.session_state.get("api_key"):
            st.error("Please enter your Gemini API Key in the sidebar.")
        elif not article_text.strip():
            st.warning("Please paste some text to summarize.")
        else:
            with st.spinner("Generating summary..."):
                try:
                    summary = summarize_health_article(article_text, st.session_state.api_key)
                    st.session_state.last_summary = summary
                    st.success("Summary generated!")

                    # Save summary with timestamp
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.summaries[timestamp] = {
                        "input": article_text,
                        "output": summary
                    }

                except Exception as e:
                    st.error(f"Error generating summary: {str(e)}")
                    summary = None

            if summary:
                st.markdown("### Summary")
                st.markdown(summary)

    # Display stored summaries
    if st.session_state.summaries:
        st.markdown("---")
        with st.expander("🗂️ View Saved Summaries"):
            for time, record in reversed(st.session_state.summaries.items()):
                st.markdown(f"**Timestamp:** {time}")
                st.markdown(f"**Input:** {record['input'][:150]}...")
                st.markdown(f"**Summary:** {record['output']}")
                st.markdown("---")

# Answer Health Question tab
with tab2:
    st.header("Ask a Health Question")
    st.markdown("Ask any general health-related question and get AI-powered suggestions.")

    use_summary_context = False
    if st.session_state.get("last_summary"):
        use_summary_context = st.checkbox("Use last article summary for context")

    question = st.text_input(
        "Your Health Question",
        placeholder="E.g., What are common treatments for seasonal allergies?",
        key="question_input"
    )

    if st.button("Get Answer", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question first.")
        elif not st.session_state.get("api_key"):
            st.error("Please enter your Gemini API Key in the sidebar.")
        else:
            context = st.session_state.last_summary if use_summary_context else None

            with st.spinner("Thinking..."):
                try:
                    answer = answer_health_question(question, context, st.session_state.api_key)
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
                    answer = None

            if answer:
                st.markdown("### Answer")
                st.markdown(answer)

# Health Tips tab
with tab3:
    st.header("Get Personalized Wellness Tips")
    st.markdown("Tell us about your goal and lifestyle to get tailored health tips.")

    col1, col2 = st.columns(2)

    with col1:
        goal = st.text_input(
            "Your Health Goal",
            placeholder="E.g., Improve sleep, lose weight, reduce stress",
            key="goal_input"
        )

    with col2:
        lifestyle = st.selectbox(
            "Your Lifestyle",
            ["Sedentary", "Moderately Active", "Very Active"]
        )

    conditions = st.text_area(
        "Any Medical Conditions or Concerns? (Optional)",
        placeholder="E.g., diabetes, back pain, anxiety",
        height=100
    )

    if st.button("Generate Health Tips", use_container_width=True):
        if not goal.strip():
            st.warning("Please enter your health goal.")
        elif not st.session_state.get("api_key"):
            st.error("Please enter your Gemini API Key in the sidebar.")
        else:
            with st.spinner("Generating tips..."):
                try:
                    tips = generate_health_tips(goal, lifestyle, conditions, st.session_state.api_key)
                except Exception as e:
                    st.error(f"Error generating tips: {str(e)}")
                    tips = None

            if tips:
                st.markdown("### Your Wellness Tips")
                st.markdown(tips)
