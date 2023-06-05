from typing import List

from langchain.schema import Document


def pretty_print_docs(docs: List[Document]):
    print(f"\n{'-' * 100}\n".join([f"Document {i + 1}:\n\n" + d.page_content for i, d in enumerate(docs)]))


def stringify_docs(docs: List[Document]):
    return f"\n".join([d.page_content for d in docs])
