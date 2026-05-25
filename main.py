import os
from fastapi import FastAPI, UploadFile, File
import shutil

from openrouter.openrouter_for_embeddings import EmbeddingService
from utils.read_csv import FileProcessor
from vectorDB.query_db import VectorDB

app = FastAPI()

db = VectorDB()
processor = FileProcessor()
embedder = EmbeddingService()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload/")
async def file_upload(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    # save file
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # process file → text
    documents = processor.process_upload(file_path)

    # embeddings
    results = embedder.generate_and_save_embeddings(documents)

    return results


@app.post("/ask/")
async def ask(query: str):
    query_embedding = embedder.generate_embedding(query)

    # similarity search for query_embedding in our VectorDB stored document embeddings
    similar_embeddings = db.search(query_embedding)
    breakpoint()
    model_response = ""
    return model_response
