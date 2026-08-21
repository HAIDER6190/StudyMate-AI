import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


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
        print("\n StudyMate AI: Sorry, something went wrong.")
        print("Please try again in a moment.")
        print(f"Error: {e}")

        return None


print("🎓 StudyMate AI")
print("Type 'exit' to stop.\n")


while True:

    question = input("You: ")

    if question.lower() == "exit":
        print("StudyMate AI: Goodbye! Keep learning 👋")
        break


    elif question.startswith("/explain"):

        topic = question.replace("/explain", "").strip()

        prompt = f"""
        Explain the following topic to a university student who is
        a beginner.

        Topic:
        {topic}

        Requirements:
        - Use simple English.
        - Explain the core idea first.
        - Give one practical example.
        - Explain important technical terms.
        """

        response = ask_studymate(prompt)


    elif question.startswith("/quiz"):

        topic = question.replace("/quiz", "").strip()

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


    else:

        response = ask_studymate(question)


    # Only print the response if the API request succeeded
    if response:
        print("\nStudyMate AI:")
        print(response.text)
        print()