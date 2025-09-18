# RAG Chatbot (Compliant & Safe)

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2.14-yellow)](https://python.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.0.48-blue?logo=networkx&logoColor=white)](https://langchain-ai.github.io/langgraph/)
![Status](https://img.shields.io/badge/Status-Experimental-orange)

This project is a simple **Retrieval-Augmented Generation (RAG) chatbot** built with **FastAPI + LangChain + Chroma + Ollama/OpenAI**.  

It demonstrates how to build a chatbot that:
- Loads documents from `data/docs/`
- Creates embeddings and stores them in a **vector database** (Chroma)
- Retrieves the most relevant chunks for each query
- Passes them into an **LLM** with a custom prompt
- Maintains **chat history** across sessions
- Exposes an API with a `/chat` endpoint for interaction
- Adds **guardrails for compliance and safety** (PII redaction, profanity filter, monitoring)

---


### Run with Docker
```bash
docker compose up --build
# UI http://localhost:8501, API http://localhost:8000
```

---


## ⚙️ Anatomy → Code Mapping

| Anatomy Part  | Folder / File                  | Description |
|---------------|--------------------------------|-------------|
| Interface     | `app/api/routes.py`            | FastAPI endpoints (`/chat`, `/sentiment`) |
| Brain         | `app/llm/providers.py`         | LLM (GPT-4o, Claude, Llama) |
| Memory        | `app/memory/vectorstore.py`    | Chroma vector DB (long-term) |
|               | `app/memory/history.py`        | Chat history per session (short-term) |
| Orchestrator  | `app/orchestration/chains.py`  | Retrieval + RAG pipeline |
| Guardrails    | `app/guardrails/prompts.py`    | Safe system prompt |
|               | `app/guardrails/filters.py`    | Strip unwanted tokens (e.g. `<think>`) |
| Tools         | `app/tools/sentiment.py`       | Extra skill (sentiment analysis) |
| Feedback      | `app/monitoring/logging.py`    | Logging stub for monitoring |

---

## 🚀 Features


- **FastAPI API** with `/health` and `/chat` endpoints
- **Retriever + LLM orchestration** using LangChain
- **Chroma Vectorstore** with embeddings from HuggingFace
- **Session-based memory** (chat history tracked by `session_id`)
- **Pluggable LLM backends** (Ollama or OpenAI)
- **Guardrails**:
  - PII redaction (SSNs, phone numbers, emails)
  - Profanity detection
  - Safe default prompts (`I don’t know` when context is missing)
- **Monitoring**:
  - Logs interactions to `logs/chat.log`
  - Collects user feedback (`feedback.jsonl`)

## 🕸️ Orchestration Options

This project supports two orchestration modes:

1. **LangChain (default)**  
   A simple linear RAG chain: retriever → LLM → answer.

2. **LangGraph (optional)**  
   A graph-based approach for more complex flows (branching, retries, guardrails, tool-calling).

Toggle via `settings.py`:

```python
use_langgraph = True
```

---

## 📂 Project Structure
```

├── api/                  # API routes + request models
│   └── routes.py
├── orchestration/        # RAG orchestration
│   └── chains.py
├── memory/               # Vectorstore + chat history
│   ├── vectorstore.py
│   └── history.py
├── guardrails/           # Prompts + filters
│   ├── prompts.py
│   └── filters.py
├── monitoring/           # Logs + feedback collection
│   ├── logging.py
│   └── evals.py
├── data/
│   ├── docs/             # Input documents (.md, .txt, .pdf)
│   └── chroma/           # Vectorstore persistence
├── llm/                  # LLM provider utils (Ollama / OpenAI)
│   └── providers.py
├── ui/                   # Streamlit chat interface
│   └── app.py
├── main.py               # FastAPI app entrypoint
├── settings.py           # Config (doc_dir, chroma_dir, models, etc.)
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone & Install
```bash
git clone https://github.com/Ali-Ismail-1/RAG-with-guardrails
cd RAG-chatbot-compliant-safe
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt -r requirements-dev.txt
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

## 5. Run with Streamlit UI:
```bash
streamlit run ui/app.py
```
Then open http://localhost:8501

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

**Guardrails**
- Redacts PII and blocks profanity
- Ensures fallback response when no context is found

**Monitoring**
- Logs every Q/A
- Collects user feedback for evaluation

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

- ✅ Current: Basic RAG pipeline (retriever + LLM + history)
- ✅ Guardrails for PII + profanity
- ✅ Monitoring (logging + feedback)
- 🔜 Add LangGraph orchestration for more complex flows  
- 🔜 Add richer UI (React or Next.js)
- 🔜 Add more advanced compliance filters
- 🔜 Support additional vector stores (Pinecone, Weaviate)  

---

## Demo 

<img width="1402" height="979" alt="image" src="https://github.com/user-attachments/assets/23324c61-5084-4cd5-96a5-a6d59a410244" />

---

## 🛡️ Disclaimer
This project is for **educational use only**.  
Before deploying in production:
- Strengthen compliance checks
- Add monitoring & logging pipelines
- Secure API endpoints
- Evaluate against real-world data

---

## 📖 References
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Ollama Models](https://ollama.ai/library)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

