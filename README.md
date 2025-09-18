# RAG Chatbot (Compliant & Safe)

This project is a simple **Retrieval-Augmented Generation (RAG) chatbot** built with **FastAPI + LangChain + Chroma + Ollama/OpenAI**.  

It demonstrates how to build a chatbot that:
- Loads documents from `data/docs/`
- Creates embeddings and stores them in a **vector database** (Chroma)
- Retrieves the most relevant chunks for each query
- Passes them into an **LLM** with a custom prompt
- Maintains **chat history** across sessions
- Exposes an API with a `/chat` endpoint for interaction

---

## 🚀 Features

- **FastAPI API** with `/health` and `/chat` endpoints
- **Retriever + LLM orchestration** using LangChain
- **Chroma Vectorstore** with embeddings from HuggingFace
- **Session-based memory** (chat history tracked by `session_id`)
- **Pluggable LLM backends** (Ollama or OpenAI)
- **Guardrails** (filters, prompts, safe defaults)

---

## 📂 Project Structure

├── api/ # API routes + request models
│ └── routes.py
├── orchestration/ # RAG orchestration
│ └── chains.py
├── memory/ # Vectorstore + chat history
│ ├── vectorstore.py
│ └── history.py
├── guardrails/ # Prompts + filters
│ ├── prompts.py
│ └── filters.py
├── data/
│ ├── docs/ # Input documents (.md, .txt, .pdf)
│ └── chroma/ # Vectorstore persistence
├── llm/ # LLM provider utils (Ollama / OpenAI)
│ └── providers.py
├── main.py # FastAPI app entrypoint
├── settings.py # Config (doc_dir, chroma_dir, models, etc.)
├── requirements.txt
└── README.md


---

## ⚙️ Setup

### 1. Clone & Install
```bash
git clone <your-repo>
cd RAG-chatbot-compliant-safe
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 2. Add Docs

Put .md, .txt, or .pdf files into:
```bash
data/docs/
```

## 3. Start Ollama (if using locally)
```powershell
ollama serve
ollama pull llama3:8b
ollama run llama3:8b
```

## 4. Run the API
```bash
uvicorn main:app --reload
```

---

## 📡 Usage

### Healthcheck
```bash
curl http://localhost:8000/health
```

### Chat
```
$json = @"
{
  "session_id": "abc",
  "question": "What docs are in here?"
}
"@

curl -Uri "http://localhost:8000/chat" `
     -Method Post `
     -Headers @{ "Content-Type" = "application/json" } `
     -Body $json

```

Response:
```json
{
  "answer": "The provided context contains documentation in the form of Python tips..."
}
```

---

## 🧩 How It Works

**Vectorstore Build**
- Loads all docs in `data/docs/`
- Splits them into chunks
- Creates embeddings via HuggingFace
- Stores vectors in **Chroma** (`data/chroma/`)

**Retriever**
- Finds the top-k relevant chunks for a query

**Prompting**
- Wraps user question + retrieved context into a safe `BASE_PROMPT`

**LLM**
- Sends the prompt to **Ollama** (default) or **OpenAI**

**Memory**
- Tracks past conversation history by `session_id`

---

## 🔧 Config

Edit `settings.py` (or use `.env`) to configure:

- `llm_provider` → `"ollama"` or `"openai"`
- `ollama_model` → `llama3:8b`, etc.
- `openai_model` → `gpt-4o-mini`, etc.
- `doc_dir` → where docs are loaded from
- `chroma_dir` → where vectors are stored
- `embeddings_model` → e.g. `"sentence-transformers/all-MiniLM-L6-v2"`

---

## 📌 Roadmap

✅ Current: Basic RAG pipeline (retriever + LLM + history)  
🔜 Add LangGraph orchestration for more complex flows  
🔜 Add UI (Streamlit or React) for a chat interface  
🔜 Add more guardrails (profanity filter, compliance checks)  
🔜 Add support for additional vector stores (Pinecone, Weaviate)  

---

## 🛡️ Disclaimer
This project is for **educational use only**.  
Before deploying in production, add compliance checks, guardrails, monitoring, and security hardening.

---

## 📖 References
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Ollama Models](https://ollama.ai/library)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

