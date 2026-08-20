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

print("🎓 StudyMate AI")
print("Type 'exit' to stop.\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        print("StudyMate AI: Goodbye! Keep learning 👋")
        break

    response = chat.send_message(
        message=question
    )

    print("\nStudyMate AI:")
    print(response.text)
    print()