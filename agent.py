import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai

def check_api_key(api_key):
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        return any("gemini" in model.name.lower() for model in models)
    except Exception:
        return False

def get_gemini_llm(api_key, temperature=0.7):
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=temperature,
        max_output_tokens=2048
    )

def summarize_health_article(text, api_key=None):
    template = """
    You are a medical writer helping the general public understand health articles.

    ARTICLE:
    {text}

    INSTRUCTIONS:
    - Use non-technical language for general understanding
    - Highlight symptoms, causes, treatments, and prevention if relevant
    - Keep it organized and easy to read

    SUMMARY:
    """

    prompt = PromptTemplate(input_variables=["text"], template=template)
    llm = get_gemini_llm(api_key, temperature=0.3)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(text=text)

def answer_health_question(question, context=None, api_key=None):
    context_section = f"\nADDITIONAL CONTEXT:\n{context}\n" if context else ""

    template = """
    You are a knowledgeable and responsible health assistant.

    QUESTION:
    {question}

    {context_section}

    INSTRUCTIONS:
    - Provide medically accurate, general health advice
    - Reference common symptoms, treatments, or wellness tips when relevant
    - If unsure, recommend seeing a healthcare provider
    - Keep responses understandable to a general audience

    ANSWER:
    """

    prompt = PromptTemplate(
        input_variables=["question", "context_section"],
        template=template
    )
    llm = get_gemini_llm(api_key, temperature=0.7)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(question=question, context_section=context_section)

def generate_health_tips(goal, lifestyle, conditions="", api_key=None):
    template = """
    You are a health coach creating personalized wellness tips.

    USER PROFILE:
    - Health Goal: {goal}
    - Lifestyle: {lifestyle}
    - Existing Conditions/Concerns: {conditions}

    INSTRUCTIONS:
    - Provide 5-7 actionable health and wellness tips
    - Tailor suggestions to the user's goal and lifestyle
    - Include advice on diet, physical activity, stress, or sleep if applicable
    - Be practical and supportive

    HEALTH TIPS:
    """

    prompt = PromptTemplate(
        input_variables=["goal", "lifestyle", "conditions"],
        template=template
    )
    llm = get_gemini_llm(api_key, temperature=0.8)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(goal=goal, lifestyle=lifestyle, conditions=conditions)
