# memory/vectorstore.py
import os
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from settings import settings

def build_or_load_vectorstore(doc_dir: str, chroma_dir: str) -> Chroma:
    os.makedirs(chroma_dir, exist_ok=True)
    docs = []

    # load supported files
    for root, _, files in os.walk(doc_dir):
        for file in files:
            path = os.path.join(root, file)
            if file.endswith((".txt",".md")):
                docs.extend(TextLoader(path, encoding="utf-8").load())
            elif file.endswith((".pdf")):
                docs.extend(PyPDFLoader(path).load())

    # split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
    splits = splitter.split_documents(docs)
    
    # create embeddings
    embeddings = get_embeddings()
    vectorstore = Chroma(persist_directory=chroma_dir, embedding_function=embeddings)
    
    # add new data to vectorstore
    if splits:
        vectorstore.add_documents(splits)
    
    return vectorstore


def get_embeddings():
    provider = os.getenv("embeddings_provider", "openai").lower()

    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        model = os.getenv("openai_embeddings_model", "text-embedding-3-small")
        return OpenAIEmbeddings(model=model, api_key=os.getenv("OPENAI_API_KEY"))

    if provider == "huggingface":
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
        except ModuleNotFoundError as e:
            raise RuntimeError(
                "embeddings_provider=huggingface but 'langchain-huggingface' "
                "is not installed in this environment."
            ) from e
        model = os.getenv("hf_embeddings_model", "sentence-transformers/all-MiniLM-L6-v2")
        return HuggingFaceEmbeddings(model_name=model)

    raise ValueError(f"Unknown embeddings_provider: {provider}")


VDB = build_or_load_vectorstore(settings.doc_dir, settings.chroma_dir)
RETRIEVER = VDB.as_retriever(search_kwargs={"k": 6})