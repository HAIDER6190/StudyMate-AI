import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client= genai.Client(
    api_key= os.getenv("GEMINI_API_KEY")
)


# Read the notes
with open("notes.txt","r", encoding="utf-8") as file:
    notes= file.read()

# Split notes into chunks
chunks= notes.split("\n\n")

print("Notes have been chunked into", len(chunks), "chunks.")

# Craete Embedding for each chunk
embeddings =[]

for chunk in chunks:
    if chunk.strip():
       result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=chunk
        )
       
       embeddings.append(result.embeddings[0].values)

print ("number of embeddings :", len(embeddings))


# Display first chunk and part of it's embedding

print("\n--- First Chunk ---")
print(chunks[0])

print("\n--- First Embedding ---")
print(embeddings[0][:10])

## Seminaticsearch

import math

def cosine_similarity(vector_a, vector_b):
    dot_product = sum( a* b for a, b in zip (vector_a, vector_b))

    magnititude_a = math.sqrt(sum(a * a for a in vector_a))
    magnititude_b = math.sqrt(sum(b * b for b in vector_b))

    return dot_product / (magnititude_a * magnititude_b)

# Ask Question 
question = input('\ntest question: ')

# Create embedding for the question
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=question
)
question_embedding = result.embeddings[0].values

## compare question with every chunk

scores = []

for i , embedding in enumerate (embeddings):
    score = cosine_similarity(question_embedding, embedding)

    scores.append((score, i))


# find the most  similar chunk 
scores.sort(reverse=True)

best_score, best_index = scores[0]

print("\n--- Most Relevant Chunk ---")
print(chunks[best_index])

print("\n--- Similarity Score ---")
print(best_score)

