import numpy
from sklearn.neighbors import NearestNeighbors

class VectorDatabase:
    def __init__(self):
        self.embeddings = []
        self.metadata = []
        self.index = None

    def add_embedding(self, embedding, metadata=None):
        self.embeddings.append(embedding)
        self.metadata.append(metadata)

    def build_index(self):
        self.index = NearestNeighbors(metric='cosine')
        self.index.fit(self.embeddings)

    def search(self, query_embedding, k=3):
        distances, indices = self.index.kneighbors([query_embedding], n_neighbors=k)
        results = [(self.metadata[i], distances[0][j]) for j, i in enumerate(indices[0])]
        return results
