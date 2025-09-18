# orchestration/chains.py
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.runnables.history import RunnableWithMessageHistory

from llm.providers import get_llm
from memory.vectorstore import RETRIEVER
from memory.history import get_history
from guardrails.prompts import BASE_PROMPT
from guardrails.filters import strip_think
from monitoring.logging import log_interaction


def make_rag_chain():
    llm = get_llm()
    doc_chain = create_stuff_documents_chain(llm, BASE_PROMPT)
    retrieval_chain = create_retrieval_chain(RETRIEVER, doc_chain)

    runnable = RunnableWithMessageHistory(
        runnable=retrieval_chain,
        get_session_history=get_history,
        input_messages_key="input",
        history_messages_key="history",
    )
    return runnable

RAG = make_rag_chain()

def ask_with_context(session_id: str, question: str) -> str:
    
    result = RAG.invoke(
        {"input": question},
        config={"configurable": {"session_id": session_id}},
    )
    answer = result.get("answer") or str(result)
    answer = strip_think(answer)
    log_interaction(session_id, question, answer)
    return answer