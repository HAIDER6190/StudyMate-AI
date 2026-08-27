import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load environment variables
load_dotenv()


# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Read study notes
with open("notes.txt", "r", encoding="utf-8") as file:
    notes = file.read()

# Chunking the notes into smaller parts
chunks = notes.split("\n\n")

# Find relevant chunk of notes based on the question
def find_relevant_chunk(question):

    question_words = question.lower().split()

    best_chunk = ""
    best_score = 0

    for chunk in chunks:

        chunk_words = chunk.lower().split()

        score = 0

        for word in question_words:

            if word in chunk_words:
                score += 1

        if score > best_score:
            best_score = score
            best_chunk = chunk

    return best_chunk


# Create conversation
chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        system_instruction="""
        You are StudyMate AI, a friendly university tutor.

        Your job is to:
        - Explain difficult topics in simple language.
        - Give practical examples.
        - Assume the student is a beginner.
        - Explain technical terminology when necessary.
        - Help students understand rather than just giving answers.
        """
    )
)


# Handle Gemini API requests
def ask_studymate(prompt):

    try:
        response = chat.send_message(message=prompt)
        return response

    except Exception as e:
        print("\nStudyMate AI: Sorry, something went wrong.")
        print("Please try again in a moment.")
        print(f"Error: {e}")

        return None


# Start StudyMate
print("🎓 StudyMate AI")
print("Type 'exit' to stop.")
print("Commands:")
print("/study <question>  - Ask about your study notes")
print("/explain <topic>   - Explain a topic")
print("/quiz <topic>      - Create a quiz")
print()


# Main conversation loop
while True:

    question = input("You: ").strip()


    # Exit
    if question.lower() == "exit":

        print("StudyMate AI: Goodbye! Keep learning 👋")
        break


    # Study notes
    elif question.startswith("/study"):

        user_question = question.replace("/study", "", 1).strip()

        if not user_question:

            print("\nStudyMate AI: Please ask a question about your notes.")
            print("Example: /study What is supervised learning?\n")
            continue

            # Find relevant chunk
        relevant_chunk = find_relevant_chunk(user_question)


        if not relevant_chunk:

            print(
                "\nStudyMate AI: I couldn't find relevant information "
                "in your notes.\n"
            )

            continue

         # Give the relevant chunk to Gemini
        prompt = f"""
        You are helping a university student study.

        Use ONLY the following relevant section from the student's notes
        to answer the question.

        RELEVANT NOTE:
        ----------------
        {relevant_chunk}
        ----------------

        STUDENT QUESTION:
        {user_question}

        Requirements:
        - Answer using only the provided note.
        - Use simple English.
        - Explain important technical terms.
        - Give a simple example when useful.
        - Do not invent information.
        - If the answer cannot be answered from the note, say:
          "I couldn't find that information in your notes."
        """

        response = ask_studymate(prompt)

    # Quiz
    elif question.startswith("/quiz"):

        topic = question.replace("/quiz", "", 1).strip()

        if not topic:

            print("\nStudyMate AI: Please provide a topic.")
            print("Example: /quiz machine learning\n")
            continue


        prompt = f"""
        Create a 5-question multiple-choice quiz about:

        {topic}

        Requirements:
        - Give 4 options for each question.
        - Do NOT show the correct answers.
        - Do NOT provide an answer key.
        - Tell the student to answer in this format:

        1-A, 2-B, 3-C, 4-D, 5-A
        """

        response = ask_studymate(prompt)


    # Normal conversation
    else:

        response = ask_studymate(question)


    # Print response if successful
    if response:

        print("\nStudyMate AI:")
        print(response.text)
        print()