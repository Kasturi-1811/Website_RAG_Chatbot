from sentence_transformers import SentenceTransformer
import chromadb

def load_model():
    """
    Load the embedding model.
    """

    model = SentenceTransformer("all-MiniLM-L6-v2")

    return model

def connect_database():
    """
    Connect to ChromaDB.
    """

    client = chromadb.PersistentClient(
        path="data/chroma_db"
    )

    collection = client.get_collection(
        "website_chunks"
    )

    return collection



def retrieve_chunks(model, collection, query, top_k=5):
    """
    Retrieve the most relevant chunks for a user query.

    Returns:
        A list of dictionaries containing source, text and distance.
    """

    # Convert question into embedding
    query_embedding = model.encode(query).tolist()

    # Search database
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_chunks = []

    for i in range(len(results["documents"][0])):

        retrieved_chunks.append({
            "source": results["metadatas"][0][i]["source"],
            "text": results["documents"][0][i],
            "distance": results["distances"][0][i]
        })

    return retrieved_chunks


if __name__ == "__main__":

    model = load_model()
    collection = connect_database()

    question = input("Ask a question: ")

    chunks = retrieve_chunks(model, collection, question)

    print("\nTop Results\n")

    for chunk in chunks:

        print("=" * 80)

        print("Source:")
        print(chunk["source"])

        print("\nChunk:")
        print(chunk["text"])

        print("\nDistance:")
        print(chunk["distance"])