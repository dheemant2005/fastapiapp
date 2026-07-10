import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY,
        temperature=0.3,
    )

    resume_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are a professional resume analyser.
     Analyse the given resume text and provide:
     1. Key Skills found
     2. Experience Level (Junior/Mid/Senior)
     3. Strengths
     4. Areas to improve
     5. Suggested Job Roles
     Keep the analysis short and structured.""",
        ),
        ("human", "{resume_text}"),
    ])

    resume_chain = resume_prompt | llm


def analyse_resume(resume_text: str) -> str:
    if not GROQ_API_KEY:
        # Minimal local fallback analysis: echo and simple keyword heuristic
        lines = [l.strip() for l in resume_text.splitlines() if l.strip()]
        snippet = " ".join(lines)[:400]
        return f"LLM not configured. Resume snippet:\n{snippet}"
    try:
        response = resume_chain.invoke({"resume_text": resume_text})
        return getattr(response, "content", str(response))
    except Exception as e:
        return f"Error analysing resume: {str(e)}"