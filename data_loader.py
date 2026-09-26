from dotenv import load_dotenv

load_dotenv()

from pathlib import Path
from typing import List, Tuple

from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader, TextLoader


def load_web_sources(urls: List[str]) -> Tuple[List[Document], List[str]]:

    documents = []
    failures = []

    for url in urls:
        url = url.strip()

        if not url:
            continue

        try:
            loader = WebBaseLoader(url)
            loaded_docs = loader.load()

            valid_docs = []

            for doc in loaded_docs:
                if not doc.page_content or not doc.page_content.strip():
                    continue

                metadata = dict(doc.metadata)

                metadata["source_type"] = "web"
                metadata["url"] = url

                if not metadata.get("title"):
                    metadata["title"] = url

                metadata["source_name"] = metadata.get(
                    "source_name",
                    metadata.get("title", url)
                )

                doc.metadata = metadata
                valid_docs.append(doc)

            if valid_docs:
                documents.extend(valid_docs)
            else:
                failures.append(f"{url} - empty content")

        except Exception as exc:
            failures.append(f"{url} - {str(exc)}")

    return documents, failures


def load_pdf_sources(pdf_directory: str = "data/pdfs") -> Tuple[List[Document], List[str]]:
    documents = []
    failures = []

    pdf_path = Path(pdf_directory)

    if not pdf_path.exists():
        return documents, []

    pdf_files = list(pdf_path.glob("*.pdf"))

    if not pdf_files:
        return documents, []

    for pdf_file in pdf_files:
        try:
            loader = PyPDFLoader(str(pdf_file))
            loaded_docs = loader.load()

            valid_docs = []

            for doc in loaded_docs:
                if not doc.page_content or not doc.page_content.strip():
                    continue

                metadata = dict(doc.metadata)

                metadata["source_type"] = "pdf"
                metadata["file_name"] = pdf_file.name
                metadata["source"] = pdf_file.name

                if "page" in metadata:
                    metadata["page_number"] = metadata["page"] + 1
                else:
                    metadata["page_number"] = None

                doc.metadata = metadata
                valid_docs.append(doc)

            if valid_docs:
                documents.extend(valid_docs)
            else:
                failures.append(f"{pdf_file.name} - empty content")

        except Exception as exc:
            failures.append(f"{pdf_file.name} - {str(exc)}")

    return documents, failures


def load_article_sources(article_directory: str = "data/articles") -> Tuple[List[Document], List[str]]:
    documents = []
    failures = []

    article_path = Path(article_directory)

    if not article_path.exists():
        return documents, []

    txt_files = list(article_path.glob("*.txt"))

    if not txt_files:
        return documents, []

    for txt_file in txt_files:
        try:
            loader = TextLoader(str(txt_file), encoding="utf-8")
            loaded_docs = loader.load()

            valid_docs = []

            for doc in loaded_docs:
                if not doc.page_content or not doc.page_content.strip():
                    continue

                metadata = dict(doc.metadata)

                metadata["source_type"] = "article"
                metadata["file_name"] = txt_file.name
                metadata["source"] = txt_file.name
                metadata["title"] = txt_file.stem.replace("_", " ").title()
                metadata["source_name"] = txt_file.name

                doc.metadata = metadata
                valid_docs.append(doc)

            if valid_docs:
                documents.extend(valid_docs)
            else:
                failures.append(f"{txt_file.name} - empty content")

        except Exception as exc:
            failures.append(f"{txt_file.name} - {str(exc)}")

    return documents, failures


def load_all_sources(
    urls: List[str],
    pdf_directory: str = "data/pdfs",
    article_directory: str = "data/articles"
) -> Tuple[List[Document], List[str]]:

    web_documents, web_failures = load_web_sources(urls)

    pdf_documents, pdf_failures = load_pdf_sources(pdf_directory)

    article_documents, article_failures = load_article_sources(article_directory)

    all_documents = web_documents + pdf_documents + article_documents
    all_failures = web_failures + pdf_failures + article_failures

    return all_documents, all_failures