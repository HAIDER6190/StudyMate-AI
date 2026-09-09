import os 
import math
from dotenv import load_dotenv
from google import genai

load_dotenv()

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

chat = client.chats.create(
    model="gemini-3.6-flash"
)

## loading study notes
with open ("notes.txt", "r", encoding="utf-8") as f:
    notes = f.read() 


# Split the notes into chunks
chunks = notes.split("\n\n")
chunks= [chunk.strip() for chunk in chunks if chunk.strip()]
chunks = chunks[:50]
print("Number of chunks:", len(chunks))

# Embedding the chunks
embeddings= []

for chunk in chunks:
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunk
    )
    embeddings.append(result.embeddings[0].values)

print("Number of embeddings:", len(embeddings))


## cosine similarity function
def cosine_similarity(vector_a, vector_b):

    dot_product =sum (a * b for a, b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    return dot_product / (magnitude_a * magnitude_b) 
# Continuous conversation
while True:

    # Ask the user a question
    question = input("\nAsk a study question: ")

    # Exit command
    if question.lower() == "exit":
        print("\nGoodbye! 👋")
        break

    # Embedding the question
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )

    question_embedding = result.embeddings[0].values

    # Compare question embedding with each chunk embedding
    scores = []

    for i, embedding in enumerate(embeddings):

        score = cosine_similarity(
            question_embedding,
            embedding
        )

        scores.append((score, i))

    # Sort highest similarity first
    scores.sort(reverse=True)

    # Retrieve top 3 chunks
    top_k = 3

    top_chunks = scores[:top_k]

    relevant_context = ""

    for score, index in top_chunks:
        relevant_context += chunks[index] + "\n\n"

    print("\n--- Retrieved Context ---")

    for score, index in top_chunks:
        print(f"Similarity Score: {score:.4f}")
        print(chunks[index])
        print()

    # Send retrieved context + question to Gemini
    prompt = f"""
    Use the following context to answer the student's question.

    CONTEXT:
    {relevant_context}

    STUDENT QUESTION:
    {question}

    Answer using the context when possible.
    Explain the answer in simple language.
    """

    response = chat.send_message(
        message=prompt
    )

    print("\n--- StudyMate AI ---")
    print(response.text)