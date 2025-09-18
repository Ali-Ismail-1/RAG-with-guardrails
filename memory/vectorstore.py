import os
from langchain_huggingface import HuggingFaceEmbeddings
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
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    splits = splitter.split_documents(docs)
    
    # create embeddings
    embeddings = HuggingFaceEmbeddings(model_name=settings.embeddings_model)
    vectorstore = Chroma(persist_directory=chroma_dir, embedding_function=embeddings)
    
    # add new data to vectorstore
    if splits:
        vectorstore.add_documents(splits)
    
    return vectorstore

VDB = build_or_load_vectorstore(settings.doc_dir, settings.chroma_dir)
RETRIEVER = VDB.as_retriever(search_kwargs={"k": 2})