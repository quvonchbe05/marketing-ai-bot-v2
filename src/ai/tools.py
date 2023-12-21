from langchain.tools import tool
from src.db.database import vectorestore


# Tool for searching information in documents
@tool
def search_from_documents(text: str):
    """When answering, answer based on the answer provided by this tool"""
    result = vectorestore.similarity_search(text, k=5)
    return result
# ----------------------------------------------/
