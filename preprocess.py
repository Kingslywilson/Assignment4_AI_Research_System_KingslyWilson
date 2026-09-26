import re
from collections import Counter
from typing import List

from langchain_core.documents import Document


def normalize_whitespace(text: str) -> str:

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    text = re.sub(r"\n{3,}", "\n\n", text)

    text = re.sub(r"[ \t]{2,}", " ", text)

    return text.strip()


def remove_repeated_headers_footers(
    documents: List[Document],
    min_occurrences: int = 3
) -> List[Document]:
    first_lines = []
    last_lines = []

    for document in documents:
        lines = [
            line.strip()
            for line in document.page_content.splitlines()
            if line.strip()
        ]

        if len(lines) >= 2:
            first_lines.append(lines[0])
            last_lines.append(lines[-1])

    first_counts = Counter(first_lines)
    last_counts = Counter(last_lines)

    repeated_headers = {
        line
        for line, count in first_counts.items()
        if count >= min_occurrences and len(line) > 2
    }

    repeated_footers = {
        line
        for line, count in last_counts.items()
        if count >= min_occurrences and len(line) > 2
    }

    cleaned_documents = []

    for document in documents:
        lines = [
            line.strip()
            for line in document.page_content.splitlines()
            if line.strip()
        ]

        if lines and lines[0] in repeated_headers:
            lines = lines[1:]

        if lines and lines[-1] in repeated_footers:
            lines = lines[:-1]

        document.page_content = "\n".join(lines).strip()

        if document.page_content:
            cleaned_documents.append(document)

    return cleaned_documents


def remove_duplicate_documents(
    documents: List[Document]
) -> List[Document]:

    seen = set()
    unique_documents = []

    for document in documents:
        normalized_content = normalize_whitespace(
            document.page_content
        )

        if not normalized_content:
            continue

        content_key = normalized_content.lower()

        if content_key in seen:
            continue

        seen.add(content_key)

        document.page_content = normalized_content
        unique_documents.append(document)

    return unique_documents


def preprocess_documents(
    documents: List[Document]
) -> List[Document]:
    cleaned_documents = []

    for document in documents:
        if not document.page_content:
            continue

        cleaned_text = normalize_whitespace(
            document.page_content
        )

        if not cleaned_text:
            continue

        document.page_content = cleaned_text

        if document.metadata is None:
            document.metadata = {}

        cleaned_documents.append(document)

    cleaned_documents = remove_repeated_headers_footers(
        cleaned_documents
    )

    cleaned_documents = remove_duplicate_documents(
        cleaned_documents
    )

    return cleaned_documents


def prepare_source_text(
    documents: List[Document],
    max_characters: int = 6000
) -> str:
    source_sections = []
    total_characters = 0

    for index, document in enumerate(documents, start=1):
        metadata = document.metadata
        source_type = metadata.get("source_type", "unknown")

        if source_type == "web":
            title = metadata.get(
                "title",
                "Untitled Web Source"
            )

            url = metadata.get(
                "url",
                metadata.get(
                    "source",
                    "Unknown URL"
                )
            )

            source_label = (
                f"Source {index}\n"
                f"Type: Web\n"
                f"Title: {title}\n"
                f"URL: {url}"
            )

        elif source_type == "pdf":
            file_name = metadata.get(
                "file_name",
                metadata.get(
                    "source",
                    "Unknown PDF"
                )
            )

            page_number = metadata.get(
                "page_number",
                metadata.get(
                    "page",
                    "Unknown"
                )
            )

            source_label = (
                f"Source {index}\n"
                f"Type: PDF\n"
                f"File: {file_name}\n"
                f"Page: {page_number}"
            )

        elif source_type == "article":
            file_name = metadata.get(
                "file_name",
                metadata.get(
                    "source",
                    "Unknown Article"
                )
            )
            title = metadata.get("title", file_name)

            source_label = (
                f"Source {index}\n"
                f"Type: Article\n"
                f"Title: {title}\n"
                f"File: {file_name}"
            )

        else:
            source = metadata.get(
                "source",
                "Unknown Source"
            )

            source_label = (
                f"Source {index}\n"
                f"Type: {source_type}\n"
                f"Source: {source}"
            )

        remaining = (
            max_characters - total_characters
        )

        if remaining <= 0:
            break

        content = document.page_content[:remaining]

        section = (
            f"{source_label}\n"
            f"Content:\n"
            f"{content}"
        )

        source_sections.append(section)

        total_characters += len(section)

    return (
        "\n\n"
        + (
            "\n\n"
            + "=" * 80
            + "\n\n"
        ).join(source_sections)
    )