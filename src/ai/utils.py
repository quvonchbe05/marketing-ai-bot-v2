from langchain.document_loaders import DirectoryLoader, NotionDBLoader
from langchain.text_splitter import CharacterTextSplitter
import json

with open('src/uploads/notions.json', 'r') as f:
    notion_integrations = json.load(f)


def get_documents(direction: str, types: list):
    documents = []

    for file_type in types:
        loader = DirectoryLoader(path=direction, glob=f"**/*.{file_type}")
        documents.extend(loader.load())

    for notion in notion_integrations:
        notion_loader = NotionDBLoader(
            integration_token=notion['token'],
            database_id=notion['database_id'],
            request_timeout_sec=30,
        )
        
        documents.extend(notion_loader.load())

    return documents


def document_splitter(documents):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    result = text_splitter.split_documents(documents)

    return result


def format_text_to_html(text):
    """
    Converts plain text to HTML with bold formatting for quoted words.

    Args:
        text: The plain text string.

    Returns:
        The HTML string with bold tags for quoted words.
    """
    text = text.replace("\n", "<br/>")
    formatted_text = []
    is_bolds = []
    for word in text.split():
        if '"' in word:
            if is_bolds and "<b>" == is_bolds[-1]:
                formatted_text.append(word.replace('"', "</b>"))
                is_bolds.append("</b>")
            else:
                formatted_text.append(word.replace('"', "<b>"))
                is_bolds.append("<b>")
        else:
            formatted_text.append(word)

    return " ".join(formatted_text)

alloweb_files = ['pdf', 'md', 'txt', 'docx', 'pptx', 'csv', 'xlsx']
documents = get_documents('./src/uploads/', alloweb_files)
ready_documetns = document_splitter(documents)