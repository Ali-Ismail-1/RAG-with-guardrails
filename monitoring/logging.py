# monitoring/logging.py
import logging

logging.basicConfig(
    filename="rag_chatbot.log",
    level=logging.INFO,
    format="%(asctime)s -  [%(levelname)s] - %(message)s"
)

logger = logging.getLogger("rag_chatbot")

def log_interaction(session_id: str, question: str, answer: str):
    logger.info(f"Session ID: {session_id}, Question: {question}, Answer: {answer}")