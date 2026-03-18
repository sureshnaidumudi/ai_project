from sentence_transformers import SentenceTransformer
import numpy as np

class VectorStore:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.docs = []
        self.embeddings = []

    def add_documents(self, docs):

        self.docs = docs
        self.embeddings = self.model.encode(docs)

    def search(self, query, k=3):

        query_vec = self.model.encode([query])[0]

        similarities = []

        for emb in self.embeddings:
            sim = np.dot(query_vec, emb) / (
                np.linalg.norm(query_vec) * np.linalg.norm(emb)
            )
            similarities.append(sim)

        top_k = sorted(range(len(similarities)),
                       key=lambda i: similarities[i],
                       reverse=True)[:k]

        return [self.docs[i] for i in top_k]