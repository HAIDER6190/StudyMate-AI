import os
import pickle
import hashlib
import faiss
import numpy as np

from dotenv import load_dotenv
from google import genai


#    
# Configuration
#    

EMBEDDINGS_FILE = "embeddings.pkl"
FAISS_FILE = "study_index.faiss"


#    
# Setup Gemini
#    

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


#    
# Better Chunking
#    

def create_chunks(
    text,
    max_chars=1000,
    overlap_paragraphs=1
):

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = []
    current_length = 0

    for paragraph in paragraphs:

        paragraph_length = len(paragraph)

        if (
            current_chunk
            and current_length + paragraph_length > max_chars
        ):

            chunks.append(
                "\n\n".join(current_chunk)
            )

            # Keep the last paragraph
            # for context overlap
            current_chunk = current_chunk[
                -overlap_paragraphs:
            ]

            current_length = sum(
                len(p) + 2
                for p in current_chunk
            )

        current_chunk.append(paragraph)

        current_length += (
            paragraph_length + 2
        )

    # Add the final chunk
    if current_chunk:

        chunks.append(
            "\n\n".join(current_chunk)
        )

    return chunks


#    
# Create FAISS Index
#    

def create_faiss_index(embeddings):

    embedding_matrix = np.array(
        embeddings,
        dtype="float32"
    )

    dimension = embedding_matrix.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        embedding_matrix
    )

    return index


#    
# Load Study Notes
#    

with open(
    "notes.txt",
    "r",
    encoding="utf-8"
) as f:

    notes = f.read()


#    
# Create Notes Fingerprint
#    

notes_hash = hashlib.md5(
    notes.encode("utf-8")
).hexdigest()


#    
# Create Better Chunks
#    

chunks = create_chunks(notes)

print(
    "Number of chunks:",
    len(chunks)
)


#    
# Load or Create Embeddings
#    

embeddings_changed = False


if os.path.exists(EMBEDDINGS_FILE):

    print(
        "Loading saved embeddings..."
    )

    with open(
        EMBEDDINGS_FILE,
        "rb"
    ) as f:

        saved_data = pickle.load(f)


    # Check whether notes changed
    if saved_data["notes_hash"] == notes_hash:

        print(
            "Notes have not changed."
        )

        chunks = saved_data["chunks"]

        embeddings = saved_data[
            "embeddings"
        ]


    else:

        print(
            "Notes have changed. "
            "Recreating embeddings..."
        )

        embeddings = []


        # Create embeddings for every chunk
        for chunk in chunks:

            result = client.models.embed_content(
                model="gemini-embedding-001",
                contents=chunk
            )

            embeddings.append(
                result.embeddings[0].values
            )


        # Save updated embeddings
        saved_data = {
            "chunks": chunks,
            "embeddings": embeddings,
            "notes_hash": notes_hash
        }


        with open(
            EMBEDDINGS_FILE,
            "wb"
        ) as f:

            pickle.dump(
                saved_data,
                f
            )


        print(
            "Embeddings updated."
        )

        embeddings_changed = True


else:

    print(
        "Creating embeddings..."
    )

    embeddings = []


    # Create embeddings for every chunk
    for chunk in chunks:

        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=chunk
        )

        embeddings.append(
            result.embeddings[0].values
        )


    # Save embeddings
    saved_data = {
        "chunks": chunks,
        "embeddings": embeddings,
        "notes_hash": notes_hash
    }


    with open(
        EMBEDDINGS_FILE,
        "wb"
    ) as f:

        pickle.dump(
            saved_data,
            f
        )


    print(
        "Embeddings saved to embeddings.pkl"
    )

    embeddings_changed = True


print(
    "Number of embeddings:",
    len(embeddings)
)


#    
# Load or Create FAISS Index
#    

if (
    embeddings_changed
    or not os.path.exists(FAISS_FILE)
):

    print(
        "Creating FAISS index..."
    )


    index = create_faiss_index(
        embeddings
    )


    print(
        "Number of vectors in FAISS:",
        index.ntotal
    )


    # Save FAISS index
    faiss.write_index(
        index,
        FAISS_FILE
    )


    print(
        "FAISS index saved."
    )


else:

    print(
        "Loading saved FAISS index..."
    )


    index = faiss.read_index(
        FAISS_FILE
    )


    print(
        "Number of vectors in FAISS:",
        index.ntotal
    )


#    
# Retrieve Relevant Chunks
#    

def retrieve_context(
    question,
    top_k=3
):

    # Create embedding for the question
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )


    question_embedding = np.array(
        [
            result.embeddings[0].values
        ],
        dtype="float32"
    )


    # Search FAISS
    distances, indices = index.search(
        question_embedding,
        top_k
    )


    # Build context
    relevant_context = ""


    for i in range(top_k):

        chunk_index = indices[0][i]

        relevant_context += (
            chunks[chunk_index]
        )

        relevant_context += "\n\n"


    return relevant_context


#    
# Ask StudyMate a Question
#    

question = input(
    "\nAsk a question: "
)


# Retrieve relevant study notes
context = retrieve_context(
    question
)


print(
    "\n--- Retrieved Context ---"
)

print(context)


#    
# Generate Answer with Gemini
#    

prompt = f"""

You are StudyMate AI, a friendly
university tutor.

Use the following study notes to answer
the student's question.

STUDY NOTES:
{context}

STUDENT QUESTION:
{question}

Instructions:

- Use the study notes when possible.
- Explain the answer in simple language.
- Assume the student is a beginner.
- Do not invent information that is not
  supported by the notes.
- If the notes do not contain enough
  information, say so.
"""


response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)


#    
# Display Answer
#    

print(
    "\n--- StudyMate AI ---"
)

print(
    response.text
)