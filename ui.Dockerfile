# ui/ui.Dockerfile
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install streamlit requests

COPY . .

EXPOSE 8501
CMD ["bash", "-lc", "streamlit run ui/app.py --server.port ${PORT:-8501} --server.address 0.0.0.0"]
