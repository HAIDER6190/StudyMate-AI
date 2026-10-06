import faiss
import numpy as np

Vectors = np.array([
    [1.0, 0.0],
    [0.0, 1.0],
    [1.0, 1.0],
    
], dtype = "float32")

index = faiss.IndexFlatL2(2)  # 2 is the dimension of the vectors

index.add(Vectors)  # Add vectors to the index

print("Number of vectors in the index:", index.ntotal)

## search 
query = np.array([
    [0.9, 0.1],
], dtype = "float32")

distances, indices= index.search(query, k=2)

print("Indices of nearest neighbors:", indices)
print("Distances to nearest neighbors:", distances)