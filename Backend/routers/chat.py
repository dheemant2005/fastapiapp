from fastapi import APIRouter
from schemas.chat import  ChatRequest, ChatResponse
from services.langchain_service import ask_career_chatbot_response

router = APIRouter()

@router.post("/ask_career", response_model=ChatResponse)
def ask_career_Chatbot(request: ChatRequest):
    ans = ask_career_chatbot_response(request.message, request.session_id)
    return ChatResponse(response=ans)