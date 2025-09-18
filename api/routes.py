# api/routes.py
from fastapi import APIRouter
from orchestration.chains import ask_with_context
from api.models import ChatRequest


router = APIRouter()

@router.get("/health")
def healthcheck():
    return {"status": "healthy"}

@router.post("/chat")
def chat(request: ChatRequest):
    return {"answer": ask_with_context(request.session_id, request.question)}