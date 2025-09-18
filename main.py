# main.py
from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Compliance-Safe RAG Chatbot")

# include API Routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to the Compliance-Safe RAG Chatbot"}