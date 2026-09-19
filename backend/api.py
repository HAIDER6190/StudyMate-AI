import os

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

from rag import retrieve_context


load_dotenv()


# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Create FastAPI app
app = FastAPI()


class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "StudyMate AI API is running!"
    }


@app.post("/ask")
def ask_question(data: Question):

    # Step 1: Retrieve relevant study notes
    context = retrieve_context(data.question)

    # Step 2: Create prompt using retrieved context
    prompt = f"""
You are StudyMate AI, a friendly university tutor.

Use the following study notes to answer the student's question.

STUDY NOTES:
{context}

STUDENT QUESTION:
{data.question}

Instructions:
- Answer using the study notes when possible.
- Explain the concept in simple language.
- Assume the student is a beginner.
- If the answer is not in the study notes, say that the notes do not contain enough information.
"""

    # Step 3: Ask Gemini
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    # Step 4: Return the answer
    return {
        "question": data.question,
        "answer": response.text
    }