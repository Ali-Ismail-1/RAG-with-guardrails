# guardrails/prompts.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

BASE_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant. Use the provided context to answer the question. "
        "If the context or chat history does not contain the answer, say 'I don't know'."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "Question: {input}\n\nContext:\n{context}"),
])