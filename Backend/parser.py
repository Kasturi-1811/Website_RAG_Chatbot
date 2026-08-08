import os
from bs4 import BeautifulSoup


# ==========================================
# Parse a single HTML file
# ==========================================
def parse_html(file_path):
    """
    Reads an HTML file and returns clean text.
    """

    # Read HTML
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Create BeautifulSoup object
    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Extract visible text
    text = soup.get_text(separator="\n")

    # Remove unnecessary blank lines
    lines = []

    for line in text.splitlines():

        line = line.strip()

        if line:
            lines.append(line)

    clean_text = "\n".join(lines)

    return clean_text


# ==========================================
# Save extracted text
# ==========================================
def save_text(text, filename):

    with open(f"data/parsed_txt/{filename}", "w", encoding="utf-8") as f:
        f.write(text)


# ==========================================
# Parse every HTML page
# ==========================================
def parse_all_html():

    folder = "data/raw_html"

    for file in os.listdir(folder):

        file_path = os.path.join(folder, file)

        print(f"Parsing {file}")

        text = parse_html(file_path)

        txt_filename = file.replace(".html", ".txt")

        save_text(text, txt_filename)

    print("\nParsing Completed.")


# ==========================================
# Run
# ==========================================

parse_all_html()