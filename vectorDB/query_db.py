import faiss
import numpy as np


class VectorDB:

    def __init__(self):
        self.index = None
        self.texts = []  # keeps FAISS order aligned

    def add(self, data_id, text, embedding):
        vector = np.array(embedding, dtype="float32").reshape(1, -1)

        if self.index is None:
            self.index = faiss.IndexFlatL2(vector.shape[1])

        self.index.add(vector)

        self.texts.append({
            "id": str(data_id),
            "text": text
        })

    def search(self, query_embedding, top_results=5):

        if self.index is None:
            return []

        query_vec = np.array(query_embedding, dtype="float32").reshape(1, -1)

        distances, indices = self.index.search(query_vec, top_results)

        results = []

        for i, idx in enumerate(indices[0]):
            if idx < len(self.texts):
                results.append({
                    "id": self.texts[idx]["id"],
                    "text": self.texts[idx]["text"],
                    "score": float(distances[0][i])
                })
        breakpoint()
        return results