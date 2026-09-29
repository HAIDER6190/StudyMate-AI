import os
import math
import pickle
import hashlib
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
# creating hash fingerprint of the notes to check if they have changed
notes_hash= hashlib.md5(
    notes.encode("utf-8")
).hexdigest()

chunks = notes.split("\n\n")
chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

# Temporary limit because of the embedding quota
chunks = chunks[:50]

print("Number of chunks:", len(chunks))


# -----------------------------
# Load or create embeddings
EMBEDDINGS_FILE= "embeddings.pkl"

if os.path.exists(EMBEDDINGS_FILE):

    print("Loading saved embeddings...")

    with open(EMBEDDINGS_FILE, "rb") as f:
        saved_data = pickle.load(f)

    # Check whether the notes have changed
    if saved_data["notes_hash"] == notes_hash:

        print("Notes have not changed.")

        chunks = saved_data["chunks"]
        embeddings = saved_data["embeddings"]

    else:

        print("Notes have changed. Recreating embeddings...")

        embeddings = []

        for chunk in chunks:

            result = client.models.embed_content(
                model="gemini-embedding-001",
                contents=chunk
            )

            embeddings.append(
                result.embeddings[0].values
            )

        saved_data = {
            "chunks": chunks,
            "embeddings": embeddings,
            "notes_hash": notes_hash
        }

        with open(EMBEDDINGS_FILE, "wb") as f:
            pickle.dump(saved_data, f)

        print("Embeddings updated.")

else:

    print("Creating embeddings...")

    embeddings = []

    for chunk in chunks:

        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=chunk
        )

        embeddings.append(
            result.embeddings[0].values
        )

    saved_data = {
        "chunks": chunks,
        "embeddings": embeddings,
        "notes_hash": notes_hash
    }

    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump(saved_data, f)

    print("Embeddings saved to embeddings.pkl")


print("Number of embeddings:", len(embeddings))




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