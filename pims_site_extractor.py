import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import json
import time
import os
from pypdf import PdfReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

BASE_URL = "https://www.pims.org.in/"
BASE_DOMAIN = urlparse(BASE_URL).netloc

OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "pages_txt"), exist_ok=True)

visited = set()
data = []

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (CollegeBotCrawler)"
})

SKIP_EXTENSIONS = (
    ".jpg", ".jpeg", ".png", ".gif", ".svg",
    ".zip", ".rar", ".exe"
)

def normalize_url(url):
    url, _ = urldefrag(url)
    parsed = urlparse(url)
    cleaned = parsed._replace(query="").geturl()
    if cleaned.endswith("/") and cleaned != BASE_URL:
        cleaned = cleaned.rstrip("/")
    return cleaned

def is_internal(url):
    return urlparse(url).netloc.endswith("pims.org.in")

def should_skip(url):
    url = url.lower()
    return any(url.endswith(ext) for ext in SKIP_EXTENSIONS)

def extract_html(url):
    try:
        r = session.get(url, timeout=15)
        r.raise_for_status()

        if "text/html" not in r.headers.get("Content-Type", ""):
            return None

        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        text = soup.get_text(separator=" ", strip=True)

        return {
            "url": url,
            "title": title,
            "content": text
        }

    except Exception as e:
        print(f"HTML error: {url} -> {e}")
        return None

def extract_pdf(url):
    try:
        r = session.get(url, timeout=20)
        r.raise_for_status()

        pdf_path = os.path.join(OUTPUT_DIR, "temp.pdf")
        with open(pdf_path, "wb") as f:
            f.write(r.content)

        reader = PdfReader(pdf_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return {
            "url": url,
            "title": "PDF Document",
            "content": text
        }

    except Exception as e:
        print(f"PDF error: {url} -> {e}")
        return None

def save_txt(entry):
    filename = entry["url"].replace("https://", "").replace("/", "_")
    filepath = os.path.join(OUTPUT_DIR, "pages_txt", filename[:200] + ".txt")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(entry["title"] + "\n\n" + entry["content"])

def crawl(max_pages=500):
    queue = [BASE_URL]

    while queue and len(visited) < max_pages:
        url = normalize_url(queue.pop(0))

        if url in visited or should_skip(url):
            continue

        visited.add(url)
        print(f"Crawling: {url}")

        if url.lower().endswith(".pdf"):
            result = extract_pdf(url)
            if result:
                data.append(result)
                save_txt(result)
            continue

        result = extract_html(url)
        if result:
            data.append(result)
            save_txt(result)

        try:
            r = session.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            for link in soup.find_all("a", href=True):
                full_url = normalize_url(urljoin(url, link["href"]))

                if is_internal(full_url) and full_url not in visited:
                    queue.append(full_url)

        except:
            pass

        time.sleep(1)

def chunk_text(text, size=1000):
    return [text[i:i+size] for i in range(0, len(text), size)]

def save_outputs():
    # RAW JSON
    with open(os.path.join(OUTPUT_DIR, "pims_knowledge_raw.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # CHUNKED JSON
    chunks = []
    for item in data:
        for chunk in chunk_text(item["content"]):
            chunks.append({
                "url": item["url"],
                "text": chunk
            })

    with open(os.path.join(OUTPUT_DIR, "pims_knowledge_chunks.json"), "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    # COMBINED TXT
    txt_path = os.path.join(OUTPUT_DIR, "pims_knowledge_bundle.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(f"\n\nURL: {item['url']}\n")
            f.write(item["title"] + "\n")
            f.write(item["content"] + "\n")

    # PDF GENERATION
    pdf_path = os.path.join(OUTPUT_DIR, "pims_knowledge_bundle.pdf")
    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    story = []

    for item in data:
        story.append(Paragraph(f"<b>{item['url']}</b>", styles["Normal"]))
        story.append(Spacer(1, 10))
        story.append(Paragraph(item["content"][:5000], styles["Normal"]))  # limit per page
        story.append(Spacer(1, 20))

    doc.build(story)

def main():
    crawl(max_pages=500)
    save_outputs()
    print("Done! Check pims_output folder")

if __name__ == "__main__":
    main()