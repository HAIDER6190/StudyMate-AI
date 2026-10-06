import os
import pickle
import faiss
import numpy as np

from dotenv import load_dotenv
from google import genai

## load environment variables
load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

#Load the saved embeddings and chunks
with open("embeddings.pkl", "rb") as f:
    saved_data = pickle.load(f)

chunks = saved_data["chunks"]
embeddings = saved_data["embeddings"]

print("Number of chunks:", len(chunks))
print("number of embeddings:", len(embeddings))

##conver embeddings to numpy array  
embedding_matrix = np.array(
    embeddings,
    dtype= "float32"
)
print("Shape of embedding matrix:", embedding_matrix.shape)

##create FAISS index
dimension = embedding_matrix.shape[1]
index = faiss.IndexFlatL2(dimension)  
index.add(embedding_matrix)
faiss.write_index(index, "faiss_index.index")
print("Number of vectors in the index:", index.ntotal)

## Ask a question
question = input("\nAsk a question: ")

## create embeddings for the question
result= client.models.embed_content(
    model="gemini-embedding-001",
    contents =question
)
question_embedding = np.array(
    [result.embeddings[0].values],
    dtype="float32"
)

## search FAISS
top_k = 3
distances, indices = index.search(
    question_embedding, top_k
    )

## build context from the top relevant chunks
relevant_context = ""
print("\nTop relevant chunks:")

for i in range(top_k):
    chunk_index = indices[0][i]
    distance = distances[0][i]
    chunk = chunks[chunk_index]

    print(f"\nDistance: {distance:.4f}")
    print(f"Chunk index: {chunk_index}")
    print(chunks[chunk_index])

    relevant_context += chunks[chunk_index]
    relevant_context += "\n\n"


## genarte answer with gemini
prompt = f"""
You are StudyMate AI, a friendly university tutor.

Use the following study notes to answer the student's question.

STUDY NOTES:
{relevant_context}

STUDENT QUESTION:
{question}

Instructions:
- Use the study notes when possible.
- Explain the answer in simple language.
- Assume the student is a beginner.
- Do not invent information that is not supported by the notes.
- If the notes do not contain enough information, say so.
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)
# Display final answer


print("\n--- StudyMate AI ---")
print(response.text)