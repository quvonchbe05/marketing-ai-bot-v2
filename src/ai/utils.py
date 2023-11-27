from langchain.document_loaders import DirectoryLoader, NotionDBLoader
from langchain.text_splitter import CharacterTextSplitter


def get_documents(direction: str, types: list):
    documents = []

    for file_type in types:
        loader = DirectoryLoader(path=direction, glob=f"**/*.{file_type}")
        documents.extend(loader.load())

    return documents


def document_splitter(documents):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    result = text_splitter.split_documents(documents)

    return result
