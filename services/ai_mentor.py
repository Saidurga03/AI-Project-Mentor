import os

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GROQ API KEY
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY was not found.\n"
        "Please add your Groq API key to the .env file."
    )


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# AI PROJECT MENTOR
# ============================================================

def ask_mentor(question):

    if not question or not question.strip():
        return "Please enter a question."


    try:

        response = client.chat.completions.create(

            # Current Groq production model
            model="openai/gpt-oss-20b",

            messages=[
                {
                    "role": "system",
                    "content": """
You are AI Project Mentor.

You help students build software and AI projects.

Your responsibilities include:

- Project idea generation
- Project planning
- Technology selection
- Python programming
- Web development
- Artificial Intelligence
- Machine Learning
- Database design
- Debugging
- Project architecture
- Feature development
- Project documentation
- Project presentation preparation

Give clear, practical, beginner-friendly explanations.

When explaining a project, organize the answer into
simple steps whenever appropriate.

Do not make explanations unnecessarily complicated.
"""
                },
                {
                    "role": "user",
                    "content": question
                }
            ],

            temperature=0.7,

            max_completion_tokens=1024
        )


        answer = response.choices[0].message.content


        if answer:
            return answer


        return "I couldn't generate a response. Please try again."


    except Exception as error:

        error_message = str(error)


        if "401" in error_message:

            return (
                "❌ Groq API authentication failed.\n\n"
                "Please check your GROQ_API_KEY in the .env file."
            )


        if "403" in error_message:

            return (
                "❌ Groq rejected the request.\n\n"
                "Please check your API key and model permissions."
            )


        if "404" in error_message:

            return (
                "❌ The selected Groq model is unavailable.\n\n"
                "Please check the model configuration."
            )


        if "429" in error_message:

            return (
                "⏳ Groq request limit reached.\n\n"
                "Please wait a moment and try again."
            )


        return f"⚠️ AI Mentor error: {error_message}"
