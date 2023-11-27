from langchain.tools import tool
from langchain.vectorstores.docarray import DocArrayInMemorySearch
from langchain.embeddings import OpenAIEmbeddings
from src.ai.utils import get_documents, document_splitter
from src.config import OPENAI_API_KEY

# Tool for searching information in documents
alloweb_files = ['pdf', 'md', 'txt', 'docx', 'pptx', 'csv', 'xlsx']

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
documents = get_documents('./src/uploads/', alloweb_files)
ready_documetns = document_splitter(documents)
vectorstore = DocArrayInMemorySearch.from_documents(ready_documetns, embeddings)


@tool
def search_from_documents(text: str):
    """When answering, answer based on the answer provided by this tool"""
    result = vectorstore.similarity_search(text, k=5)
    return result
# ----------------------------------------------/
