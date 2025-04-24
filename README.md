# 🩺 Gemini-Powered Health Assistant

An AI-powered virtual health assistant built using Google's Gemini API and LangChain. This assistant is designed to help users by:

- 📰 **Summarizing health articles** into easy-to-understand summaries.
- 🩺 **Answering general health-related questions** with responsible and accessible guidance.
- 💡 **Providing personalized wellness tips** based on user lifestyle and goals.

---
## 🔧 Features

- **Health Article Summarization**: Understand complex health content quickly.
- **Health Q&A Engine**: Ask any wellness or general health question and receive AI-powered advice.
- **Wellness Tips Generator**: Get health tips tailored to your lifestyle, conditions, and goals.

---
## 🛠️ Tech Stack

- **Gemini 1.5**: Accessed via `google-generativeai` for generating health insights.
- **LangChain**: Used to structure LLM interactions for various use cases.
- **Streamlit**: Provides a sleek and interactive user interface.
- **Python**: Backend development language.

---
## 🔐 How to Use

1. Visit the deployed app (or run it locally).
2. Enter your Gemini API key in the sidebar.
3. Interact with the assistant to:
   - Summarize a health article
   - Ask a general health question
   - Get personalized health tips

---
## 🚀 Run Locally

1. Clone the repository.
2. Create a `.env` file and store your Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

---
## 📦 Requirements

- streamlit
- langchain
- langchain-google-genai
- google-generativeai
- python-dotenv

---
## 🌟 Why Use This Project?

- **No medical jargon**: Clear and general language ideal for all users.
- **AI-Powered Insight**: Based on Google's Gemini for high-quality, contextual responses.
- **Personalized**: Wellness tips are based on lifestyle and goals, not generic.

---
## 📬 Contact

For feedback, suggestions, or collaboration:
- **Developer**: Sambhav Rawani
- **Email**: [Sambhav Rawani](mailto:sambhavrawani@gmail.com)

---
Stay healthy! 💚

