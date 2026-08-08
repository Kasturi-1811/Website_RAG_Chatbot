import os

from groq import Groq
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_answer(question, retrieved_chunks):

    context = ""

    for chunk in retrieved_chunks:

        context += f"Source: {chunk['source']}\n"
        context += chunk["text"]
        context += "\n\n"

    prompt = f"""
You are an AI assistant for Jeevana Kasturi's portfolio.

Answer ONLY from the provided context.

If the answer is not present in the context,
say:
"I couldn't find that information in the portfolio."

Context:

{context}

Question:

{question}

Answer:
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2

    )

    return response.choices[0].message.content