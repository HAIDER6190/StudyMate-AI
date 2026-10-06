# StudyMate AI 🎓🤖

StudyMate AI is a beginner-friendly **Generative AI learning project** that I am building while learning how Large Language Models (LLMs) and modern AI applications work technically.

The goal of this project is to build an AI-powered study assistant that can help students understand difficult topics, ask follow-up questions, summarize study materials, generate quizzes, and eventually interact with uploaded documents using RAG.

Instead of only studying Generative AI theory, I am building StudyMate AI step-by-step and documenting what I learn each day.

## 🎯 Project Goal

The final version of StudyMate AI will allow students to:

* Ask questions about different study topics
* Receive beginner-friendly explanations
* Continue conversations with context
* Summarize notes
* Generate quizzes
* Upload PDF documents
* Ask questions about uploaded documents
* Use Retrieval-Augmented Generation (RAG)
* Create study plans
* Eventually use a web interface

## 🧠 What I Am Learning

Through this project, I am learning:

* Generative AI
* Large Language Models (LLMs)
* Prompt engineering
* LLM APIs
* System instructions
* Conversation history and context
* Embeddings
* Vector databases
* Retrieval-Augmented Generation (RAG)
* AI agents and tool calling
* Python backend development
* FastAPI
* React integration
* AI application architecture

## 🛠️ Technologies

Currently using:

* Python
* Google Gemini API
* Google GenAI Python SDK
* python-dotenv

Planned technologies:

* FastAPI
* React
* PDF processing libraries
* Embeddings
* Vector database such as FAISS or Chroma
* RAG

---

# 📅 Development Journey

## Day 1 — My First LLM Application ✅

### What I Learned

On Day 1, I learned how a Python application communicates with an existing Large Language Model through an API.

The basic architecture is:

```text
Student
   ↓
Python Application
   ↓
Gemini API
   ↓
Large Language Model
   ↓
Generated Response
   ↓
StudyMate AI
```

I learned the difference between:

* An LLM
* A prompt
* An API
* An API key
* A model response

I also learned an important distinction:

> I am not training or building an LLM from scratch. I am building an application that uses an existing LLM through an API.

### First Feature — Ask StudyMate

The first version allowed the user to enter one question and receive an AI-generated answer.

Example:

```text
Ask StudyMate AI: Explain deep learning in simple terms.
```

StudyMate then sends the question to Gemini and prints the generated response.

### Added a System Instruction

I then gave StudyMate its own role.

StudyMate is instructed to behave like a friendly university tutor that:

* Explains difficult topics simply
* Gives practical examples
* Assumes the student is a beginner
* Avoids unnecessary technical jargon
* Explains technical terminology when necessary

This taught me the difference between:

```text
System Instruction
        ↓
Defines how the AI should behave

User Prompt
        ↓
Defines what the user is asking
```

### Added Continuous Chat

Originally the program stopped after answering one question.

I added a Python loop so StudyMate can continue running:

```text
Question
   ↓
Answer
   ↓
Question
   ↓
Answer
   ↓
Question
   ↓
...
```

The user can type:

```text
exit
```

to stop the application.

### Added Conversation Context

I changed the application from individual LLM requests to a Gemini chat session.

This allows StudyMate to understand previous messages.

Example:

```text
You: My name is Haider.

StudyMate AI:
Nice to meet you, Haider!

You: I am studying machine learning.

StudyMate AI:
...

You: What is my name?

StudyMate AI:
Your name is Haider.
```

This helped me understand how **conversation history and context** work in LLM applications.

### Concepts Learned on Day 1

* LLM API integration
* API authentication
* Environment variables
* Protecting API keys with `.env`
* Prompting
* System instructions
* Multi-turn conversations
* Chat history
* Context
* Python loops
* Basic error debugging

---

# 🚧 Current Version

StudyMate AI can currently:

* ✅ Connect to Gemini through an API
* ✅ Accept questions from the terminal
* ✅ Generate AI responses
* ✅ Behave like a university tutor
* ✅ Continue chatting without restarting the program
* ✅ Remember earlier messages during the current conversation
* ✅ Exit using an `exit` command

Current limitation:

Conversation memory only exists during the current running session. If the program is restarted, the previous conversation is lost.

---

# 🗺️ Roadmap

## Day 2

Planned features:

* Better prompt engineering
* Summarize study material
* Generate quizzes
* Generate explanations at different difficulty levels
* Improve StudyMate commands

## Day 3

Planned features:

* Upload/read PDF files
* Extract text from PDFs
* Split documents into chunks

## Day 4

Planned features:

* Learn embeddings
* Learn vector databases
* Build semantic search
* Implement RAG
* Chat with uploaded PDFs

## Day 5

Planned features:

* AI tools
* Function calling
* Study tools
* Smarter StudyMate workflows

## Day 6

Planned features:

* FastAPI backend
* React frontend
* Connect the frontend to the AI backend

## Day 7

Planned work:

* Improve UI
* Clean the project structure
* Add error handling
* Improve documentation
* Prepare a project demo
* Prepare to explain the architecture in an interview

---

# 🔐 Environment Variables

Create a `.env` file inside the backend folder:

```env
GEMINI_API_KEY=your_api_key_here
```

Never upload your `.env` file or API keys to GitHub.

Add the following to `.gitignore`:

```text
.env
venv/
__pycache__/
```

---

# ▶️ Running the Project

Create and activate a Python virtual environment.

Install the required packages:

```bash
pip install google-genai python-dotenv
```

Then run:

```bash
python main.py
```

Example:

```text
🎓 StudyMate AI
Type 'exit' to stop.

You: Explain neural networks in simple terms.

StudyMate AI:
...
```

---

# 📚 Why I Am Building This

Generative AI is a large field, and learning only from tutorials can make the concepts feel complicated.

I decided to learn by building.

Every day I will add a new feature to StudyMate AI and document:

* What I learned
* What I built
* Problems I encountered
* How I solved them
* New GenAI concepts I discovered

The goal is to understand not only **what Generative AI can do**, but also **how GenAI applications are built technically**.
# 📌 Project Status

**Day 1 completed ✅**
**Day 2 completed ✅**
**Day 3 completed ✅**
**Day 4 completed ✅**
**Day 5 completed ✅**
**Day 6 completed ✅**
**Day 7 completed ✅**
**Day 8 completed ✅**
**Day 9 completed ✅**



Current focus:

**Generative AI → LLM APIs → Prompting → Conversation Context → AI Features → Documents → Chunking → Embeddings → Semantic Search → RAG → FastAPI → Gemini Integration → Persistent Embeddings → FAISS → Vector Search → Persistent FAISS Index → Better Chunking → Better Retrieval**

Next:

**AI Tools → Function Calling → Tool Integration → Advanced StudyMate Features**


