from bs4 import BeautifulSoup

def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
        tag.decompose()
    return soup.get_text(separator="\n")

def remove_boilerplate_lines(text):
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        line = line.strip()
        if line and not any(kw in line.lower() for kw in ["related article", "subscribe", "click here", "reuters", "follow us"]):
            cleaned.append(line)
    return "\n".join(cleaned)

def trim_head_tail(text, head=3, tail=3):
    lines = text.strip().split("\n")
    lines = lines[head: len(lines)-tail]
    return "\n".join(lines)

def paragraph_based_chunking(paragraphs, max_words=150):
    chunks = []
    current_chunk = []
    current_len = 0

    for para in paragraphs:
        words = para.split()
        if current_len + len(words) <= max_words:
            current_chunk.append(para)
            current_len += len(words)
        else:
            chunks.append("\n\n".join(current_chunk))  # Keep paragraph separation
            current_chunk = [para]
            current_len = len(words)

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


# final_chunks = [chunk for chunk in chunks if len(chunk.split()) > 30]
