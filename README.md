# Product Search RAG

Simple product search with AI recommendations.

## Files

- `config.py` - Configuration settings
- `services.py` - All services (embeddings, LLM, vector store)
- `app.py` - FastAPI server
- `streamlit_app.py` - Streamlit UI
- `requirements.txt` - Dependencies

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your OpenRouter API key in `.env`:
```env
OPENROUTER_API_KEY=your_key_here
```

3. Start Milvus:
```bash
docker-compose up -d
```

## Run

**API Server:**
```bash
fastapi app:
- uvicorn main:app --reload
- http://127.0.0.1:8000

streamlit:
- streamlit run streamlit_app.py
- http://localhost:8501/

attu
- docker compose up
- http://127.0.0.1:3001/

```

**Streamlit UI:**
```bash
streamlit run streamlit_app.py
```

## CSV Format

```csv
product_id,product_name,category,price,features,description
PROD001,Wireless Headphones,Electronics,99.99,Bluetooth 5.0,Great sound
```

## Flow

1. Upload CSV → Process → Generate embeddings → Store in Milvus
2. User searches → Query embedding → Similarity search → Get top products → LLM recommendation
