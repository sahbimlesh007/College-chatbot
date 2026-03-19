import json
from typing import List

from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings


# Load Data From JSON File
def load_json_file(json_path: str) -> List[Document]:
    """
    Load JSON data and convert it into LangChain Document objects.

    Expected JSON format:
    [
        {
            "text": "some content",
            "url": "source link"
        },
        ...
    ]
    """
    documents: List[Document] = []

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, item in enumerate(data):
        text = item.get("text", "").strip()
        url = item.get("url", "")

        if text:  # skip empty text
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": url,
                        "chunk_id": i
                    }
                )
            )

    return documents


# Download the Embeddings from HuggingFace
def download_hugging_face_embeddings():
    """
    Download and return the HuggingFace embeddings model.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},   # change to 'cuda' if GPU
        encode_kwargs={"normalize_embeddings": True}
    )
    return embeddings