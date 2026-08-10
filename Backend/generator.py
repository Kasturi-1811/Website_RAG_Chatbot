import os

from groq import Groq
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


# Create Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(question, retrieved_chunks):

    # -----------------------------------------
    # Build context from retrieved chunks
    # -----------------------------------------

    context = ""

    for i, chunk in enumerate(retrieved_chunks, start=1):

        context += f"""
--- Context {i} ---
Source: {chunk["source"]}

{chunk["text"]}

"""


    # -----------------------------------------
    # RAG Prompt
    # -----------------------------------------

    prompt = f"""
    You are the AI assistant for Jeevana Kasturi's personal portfolio website.

    Answer the user's question using ONLY the information explicitly
    provided in the portfolio context.

    RULES:

    1. Never invent, assume, or guess information.

    2. If the answer cannot be found in the context, respond exactly:
    "I couldn't find that information in the portfolio."

    3. Give a direct and natural answer. Do not copy entire chunks.

    4. When the answer contains TWO OR MORE separate items, ALWAYS use
    a Markdown bullet list.

    5. NEVER put multiple separate items into one paragraph.

    6. For lists of projects, certifications, skills, technologies,
    internships, or features, use this format:

    - **Item 1** — short description
    - **Item 2** — short description
    - **Item 3** — short description

    7. If there is only ONE item, use a normal paragraph.

    8. Keep the answer concise. Do not unnecessarily repeat information.

    9. Do not mention ChromaDB, embeddings, vector databases, similarity
    search, retrieved chunks, RAG, distances, or internal processing.

    10. Only claim technologies, projects, companies, experience, or skills
    that are explicitly supported by the context.

    PORTFOLIO CONTEXT:

    {context}

    USER QUESTION:

    {question}

    ANSWER:
    """

    # -----------------------------------------
    # Generate answer using Groq
    # -----------------------------------------

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a factual portfolio assistant. "
                    "You must strictly follow the provided "
                    "portfolio context."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2,

        max_tokens=300
    )


    # -----------------------------------------
    # Return final answer
    # -----------------------------------------

    return response.choices[0].message.content.strip()