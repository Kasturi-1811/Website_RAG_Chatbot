import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque


# =====================================================
# Download a webpage
# =====================================================
def download_page(url):
    """
    Downloads a webpage and returns its HTML.
    """

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.text

        else:
            print(f"Failed to download: {url}")
            print("Status Code:", response.status_code)

    except Exception as e:
        print("Error:", e)

    return None


# =====================================================
# Convert URL into filename
# =====================================================
def get_filename(url):
    """
    Converts URL into a valid filename.

    Examples:
        /               -> index.html
        /about          -> about.html
        /project-1      -> project-1.html
        /blog/python    -> blog_python.html
    """

    parsed = urlparse(url)

    path = parsed.path

    if path == "" or path == "/":
        return "index.html"

    path = path.lstrip("/")

    path = path.replace("/", "_")

    return path + ".html"


# =====================================================
# Save HTML
# =====================================================
def save_html(html, filename):
    """
    Saves HTML inside data/raw_html/
    """

    with open(f"data/raw_html/{filename}", "w", encoding="utf-8") as f:
        f.write(html)


# =====================================================
# Extract Links
# =====================================================
def extract_links(html, base_url):
    """
    Extract all internal and external links.

    Returns:
        internal_links
        external_links
    """

    soup = BeautifulSoup(html, "html.parser")

    internal_links = []
    external_links = []

    base_domain = urlparse(base_url).netloc

    for tag in soup.find_all("a", href=True):

        href = tag["href"]

        # Ignore anchors and special links
        if href.startswith(("#", "mailto:", "javascript:", "tel:")):
            continue

        full_url = urljoin(base_url, href)

        current_domain = urlparse(full_url).netloc

        if current_domain == base_domain:

            if full_url not in internal_links:
                internal_links.append(full_url)

        else:

            text = tag.get_text(strip=True)

            # Some websites use icons instead of text
            if not text:
                img = tag.find("img")

                if img:
                    text = img.get("alt", "")

            external_links.append({
                "text": text,
                "url": full_url
            })

    return internal_links, external_links


# =====================================================
# Main Website Crawler
# =====================================================
def crawl_website(start_url):
    """
    Crawl every internal page of a website.
    """

    queue = deque()

    visited = set()

    all_external_links = []

    queue.append(start_url)

    while queue:

        current_url = queue.popleft()

        if current_url in visited:
            continue

        print(f"\n Crawling: {current_url}")

        visited.add(current_url)

        # ------------------------
        # Download page
        # ------------------------

        html = download_page(current_url)

        if html is None:
            continue

        # ------------------------
        # Save HTML
        # ------------------------

        filename = get_filename(current_url)

        save_html(html, filename)

        print(f" Saved as {filename}")

        # ------------------------
        # Extract Links
        # ------------------------

        internal_links, external_links = extract_links(html, current_url)

        # Store external links
        all_external_links.extend(external_links)

        # ------------------------
        # Add new pages to queue
        # ------------------------

        for link in internal_links:

            if link not in visited:
                queue.append(link)

    return visited, all_external_links


# =====================================================
# Run
# =====================================================

url = "https://jeevanakasturi-portfolio.netlify.app/"

visited_pages, external_links = crawl_website(url)

print("\n============================")
print("Visited Pages")
print("============================")

for page in visited_pages:
    print(page)

print("\n============================")
print("External Links")
print("============================")

for link in external_links:
    print(link)