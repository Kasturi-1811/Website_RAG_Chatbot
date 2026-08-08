import os
import json


# ==========================================
# Read text file
# ==========================================
def read_text(file_path):
    """
    Reads a parsed text file.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# ==========================================
# Create chunks
# ==========================================
def create_chunks(text, source, chunk_size=800):
    """
    Splits text into paragraph-based chunks.
    """

    paragraphs = text.split("\n\n")

    chunks = []

    current_chunk = ""

    chunk_id = 1

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # Can we add this paragraph?
        if len(current_chunk) + len(paragraph) <= chunk_size:

            current_chunk += paragraph + "\n\n"

        else:

            if current_chunk:

                chunks.append({
                    "chunk_id": chunk_id,
                    "source": source,
                    "text": current_chunk.strip()
                })

                chunk_id += 1

            current_chunk = paragraph + "\n\n"

    # Save last chunk
    if current_chunk:

        chunks.append({
            "chunk_id": chunk_id,
            "source": source,
            "text": current_chunk.strip()
        })

    return chunks


# ==========================================
# Save chunks
# ==========================================
def save_chunks(chunks, filename):

    os.makedirs("data/chunks", exist_ok=True)

    output_file = os.path.join("data/chunks", filename)

    with open(output_file, "w", encoding="utf-8") as f:

        json.dump(chunks, f, indent=4, ensure_ascii=False)


# ==========================================
# Chunk every parsed file
# ==========================================
def chunk_all_files():

    folder = "data/parsed_txt"

    for file in os.listdir(folder):

        print(f"Chunking {file}")

        file_path = os.path.join(folder, file)

        text = read_text(file_path)

        chunks = create_chunks(text, file)

        output_name = file.replace(".txt", "_chunks.json")

        save_chunks(chunks, output_name)

    print("\nChunking Completed.")


# ==========================================
# Run
# ==========================================

chunk_all_files()