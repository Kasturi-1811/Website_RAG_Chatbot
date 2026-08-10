from sentence_transformers import SentenceTransformer
import chromadb

def load_model():
    """
    Load the embedding model.
    This model converts text into vector embeddings.
    """

    model = SentenceTransformer("all-MiniLM-L6-v2")

    return model

def store_embeddings(model, collection, chunks, batch_size=32):
    """
    Generate embeddings in batches and store them in ChromaDB.

    Args:
        model: Loaded SentenceTransformer model.
        collection: ChromaDB collection.
        chunks: List of chunk dictionaries.
        batch_size: Number of chunks to process at once.
    """

    total_chunks = len(chunks)

    for start in range(0, total_chunks, batch_size):

        # Select one batch
        batch = chunks[start:start + batch_size]

        # Extract text from every chunk
        texts = [chunk["text"] for chunk in batch]

        # Generate embeddings for the entire batch
        embeddings = model.encode(texts).tolist()

        # Prepare data for ChromaDB
        ids = []
        documents = []
        metadatas = []

        for chunk in batch:

            ids.append(f'{chunk["source"]}_{chunk["chunk_id"]}')

            documents.append(chunk["text"])

            metadatas.append({
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"]
            })

        # Store everything in ChromaDB
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print(f"Stored {start + len(batch)} / {total_chunks} chunks")
import json
import os


def read_chunk_files():
    """
    Read all chunk JSON files from the chunks folder.
    """

    all_chunks = []

    chunk_folder = "data/chunks"

    for filename in os.listdir(chunk_folder):

        if filename.endswith(".json"):

            file_path = os.path.join(chunk_folder, filename)

            with open(file_path, "r", encoding="utf-8") as f:

                chunks = json.load(f)

                all_chunks.extend(chunks)

    return all_chunks


def connect_database():
    """
    Create or connect to the ChromaDB database.
    """

    # Get the project root directory
    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    # Build path to ChromaDB
    chroma_path = os.path.join(
        base_dir,
        "data",
        "chroma_db"
    )

    client = chromadb.PersistentClient(
        path=chroma_path
    )

    collection = client.get_or_create_collection(
        name="website_chunks"
    )

    return collection

if __name__ == "__main__":

    model = load_model()
    print("Embedding model loaded successfully.")

    collection = connect_database()
    print("Connected to ChromaDB successfully.")

    chunks = read_chunk_files()

    print(f"Total chunks : {len(chunks)}")

    store_embeddings(model, collection, chunks)

    print("\nAll chunks stored successfully!")