import os
import math
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# -----------------------------
# Load study notes
# -----------------------------

with open("notes.txt", "r", encoding="utf-8") as f:
    notes = f.read()

chunks = notes.split("\n\n")
chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

# Temporary limit because of the embedding quota
chunks = chunks[:50]

print("Number of chunks:", len(chunks))


# -----------------------------
# Create embeddings
# -----------------------------

embeddings = []

for chunk in chunks:

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunk
    )

    embeddings.append(
        result.embeddings[0].values
    )

print("Number of embeddings:", len(embeddings))


# -----------------------------
# Cosine similarity
# -----------------------------

def cosine_similarity(vector_a, vector_b):

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    return dot_product / (magnitude_a * magnitude_b)


# -----------------------------
# Retrieve relevant chunks
# -----------------------------

def retrieve_context(question, top_k=3):

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )

    question_embedding = result.embeddings[0].values

    scores = []

    for i, embedding in enumerate(embeddings):

        score = cosine_similarity(
            question_embedding,
            embedding
        )

        scores.append((score, i))

    scores.sort(reverse=True)

    top_chunks = scores[:top_k]

    relevant_context = ""

    for score, index in top_chunks:

        relevant_context += chunks[index]
        relevant_context += "\n\n"

    return relevant_context