from flask import Flask, request, jsonify
from flask_cors import CORS

from embedder import load_model, connect_database
from retriever import retrieve_chunks
from generator import generate_answer


# --------------------------------------------------
# Create Flask application
# --------------------------------------------------

app = Flask(__name__)

# Allow requests from your portfolio frontend
CORS(app)


# --------------------------------------------------
# Load RAG components once when the server starts
# --------------------------------------------------

print("Loading embedding model...")

model = load_model()

print("Connecting to ChromaDB...")

collection = connect_database()

print("RAG system ready!")


# --------------------------------------------------
# Chat API
# --------------------------------------------------

@app.route("/chat", methods=["POST"])
def chat():

    # Get JSON data sent by the frontend
    data = request.get_json()

    # Get user's question
    question = data.get("question", "").strip()

    # Make sure question is not empty
    if not question:
        return jsonify({
            "error": "Question cannot be empty."
        }), 400

    try:

        # ------------------------------------------
        # Step 1: Retrieve relevant chunks
        # ------------------------------------------

        retrieved_chunks = retrieve_chunks(
            model,
            collection,
            question,
            top_k=5
        )

        # ------------------------------------------
        # Step 2: Generate final answer using Groq
        # ------------------------------------------

        answer = generate_answer(
            question,
            retrieved_chunks
        )

        # ------------------------------------------
        # Step 3: Send answer back to frontend
        # ------------------------------------------

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        print("Error:", e)

        return jsonify({
            "error": "Something went wrong while processing the question."
        }), 500


# --------------------------------------------------
# Run Flask server
# --------------------------------------------------

if __name__ == "__main__":

    import os

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )