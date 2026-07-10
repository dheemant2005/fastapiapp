import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY,
        temperature=0.5,
    )

    prompt_with_memory = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful career guidance assistant."),
        ("human", "{user_query}")
    ])

    chain_with_memory = prompt_with_memory | llm


def ask_career_chatbot_response(question: str, session_id: str = "default") -> str:
    if not GROQ_API_KEY:
        return "LLM not configured. Set GROQ_API_KEY in .env to enable chatbot."
    try:
        response = chain_with_memory.invoke({"user_query": question})
        return getattr(response, "content", str(response))
    except Exception as e:
        return f"Error contacting LLM: {str(e)}"
