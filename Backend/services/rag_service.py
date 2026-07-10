import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from services.qdrant_service import search_jobs

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY,
        temperature=0.3,
    )
    rag_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are a job search assistant. Use the following job listings retrieved from the database to answer the question. If no relevant jobs are found, say so clearly.
     
     Retrieved Jobs:
     {context}""",
        ),
        ("human", "{question}"),
    ])

    rag_chain = rag_prompt | llm


def rag_job_search(question: str) -> str:
    results = search_jobs(question, top_k=5)
    if not results:
        return "No jobs found in the database. Please embed jobs first using the /rag/embed-jobs endpoint."
    context = "\n".join(
        [
            f"-{r['title']}: {r.get('description')} (Salary: {r.get('salary')}, Match: {r.get('score')})"
            for r in results
        ]
    )
    if not GROQ_API_KEY:
        return f"RAG not configured (no GROQ_API_KEY). Context used:\n{context}"
    try:
        response = rag_chain.invoke({"context": context, "question": question})
        return getattr(response, "content", str(response))
    except Exception as e:
        return f"Error generating RAG answer: {str(e)}"