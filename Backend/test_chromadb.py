import chromadb

# Connect to the existing database
client = chromadb.PersistentClient(path="data/chroma_db")

# Open the collection
collection = client.get_collection("website_chunks")

# Retrieve first 10 records
results = collection.get(
    limit=10,
    include=["documents", "embeddings", "metadatas"]
)

print(f"Total Records Retrieved: {len(results['ids'])}")

for i in range(len(results["ids"])):

    print("=" * 80)

    print("ID:")
    print(results["ids"][i])

    print("\nSource:")
    print(results["metadatas"][i]["source"])

    print("\nChunk ID:")
    print(results["metadatas"][i]["chunk_id"])

    print("\nDocument:")
    print(results["documents"][i])

    print("\nEmbedding Length:")
    print(len(results["embeddings"][i]))

    print("\nFirst 10 Embedding Values:")
    print(results["embeddings"][i][:10])

print("=" * 80)