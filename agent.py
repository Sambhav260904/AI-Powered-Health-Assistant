# agent.py
import os
import logging

# Try to import PromptTemplate and LLMChain from newer langchain_core first (v1.x),
# otherwise fall back to older langchain paths (v0.x).
try:
    from langchain_core.prompts import PromptTemplate
    from langchain_core.chains import LLMChain
    logging.info("Using langchain_core imports")
except Exception:
    try:
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        logging.info("Using langchain (legacy) imports")
    except Exception as e:
        raise ImportError(
            "Could not import PromptTemplate/LLMChain from langchain. "
            "Ensure a compatible langchain/langchain_core is installed."
        ) from e

# Chat wrapper for langchain-google-genai (optional). If not available, app will still try using google.generativeai directly.
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except Exception:
    # It's okay if this import fails; we'll surface a clear error later if needed.
    ChatGoogleGenerativeAI = None

import google.generativeai as genai

def check_api_key(api_key):
    """Verify the Gemini API key by listing models (best-effort)."""
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        return any("gemini" in getattr(m, "name", "").lower() for m in models)
    except Exception:
        return False

def get_gemini_llm(api_key, temperature=0.7, max_output_tokens=2048):
    """
    Return a langchain-compatible LLM wrapper if available, otherwise raise clear error.
    If ChatGoogleGenerativeAI is present, use it; otherwise return None and
    the calling code can use google.generativeai directly.
    """
    if ChatGoogleGenerativeAI is not None:
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=temperature,
            max_output_tokens=max_output_tokens
        )
    # If langchain google adapter isn't available, we will still let the calling code use genai directly.
    return None

def summarize_health_article(text, api_key=None):
    """
    Generate a user-friendly summary for a health-related article text.
    Uses langchain if a ChatGoogleGenerativeAI-backed LLM is available; otherwise uses google.generativeai directly.
    """
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

    if llm is not None:
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(text=text)
    else:
        # Fallback direct call using google.generativeai
        genai.configure(api_key=api_key)
        response = genai.generate_text(model="gemini-1.5", prompt=template.format(text=text))
        # response shape may vary; try to extract text safely
        return getattr(response, "output", getattr(response, "text", str(response)))

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
    prompt = PromptTemplate(input_variables=["question", "context_section"], template=template)
    llm = get_gemini_llm(api_key, temperature=0.7)

    if llm is not None:
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(question=question, context_section=context_section)
    else:
        genai.configure(api_key=api_key)
        full_prompt = template.format(question=question, context_section=context_section)
        response = genai.generate_text(model="gemini-1.5", prompt=full_prompt)
        return getattr(response, "output", getattr(response, "text", str(response)))

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
    prompt = PromptTemplate(input_variables=["goal", "lifestyle", "conditions"], template=template)
    llm = get_gemini_llm(api_key, temperature=0.8)

    if llm is not None:
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(goal=goal, lifestyle=lifestyle, conditions=conditions)
    else:
        genai.configure(api_key=api_key)
        full_prompt = template.format(goal=goal, lifestyle=lifestyle, conditions=conditions)
        response = genai.generate_text(model="gemini-1.5", prompt=full_prompt)
        return getattr(response, "output", getattr(response, "text", str(response)))

