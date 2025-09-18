# orchestration/graph.py
from langgraph.graph import StateGraph
from langchain.chains.combine_documents import create_stuff_documents_chain
from guardrails.filters import contains_profanity, redact_pii, strip_think
from guardrails.prompts import BASE_PROMPT
from llm.providers import get_llm
from memory.vectorstore import RETRIEVER
from monitoring.logging import log_interaction


def make_rag_graph():
    llm = get_llm()
    doc_chain = create_stuff_documents_chain(llm, BASE_PROMPT)

    # define the graph
    graph = StateGraph()

    # nodes
    graph.add_node("retrieval", RETRIEVER)
    graph.add_node("generate", doc_chain)

    # edges
    graph.add_edge("retrieval", "generate")

    # entry/exit
    graph.add_entry_point("retrieval")
    graph.set_finish_point("generate")

    # compile the graph
    return graph.compile()

# instantiate the graph
RAG_GRAPH = make_rag_graph()


def ask_with_graph(session_id: str, question: str) -> str:

    if contains_profanity(question):
        return "Inappropriate content detected."
        
    result = RAG_GRAPH.invoke(
        {"input": question}, 
        config={"configurable": {"session_id": session_id}}
    )
    
    answer = result.get("answer") or str(result)
    answer = strip_think(answer)
    answer = redact_pii(answer)
    log_interaction(session_id, question, answer)
    return answer