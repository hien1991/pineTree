import os
import tempfile
from werkzeug.datastructures import FileStorage
import tiktoken
from langchain.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    CSVLoader,
    UnstructuredImageLoader
)
from database import Database
from langchain.text_splitter import RecursiveCharacterTextSplitter


tokenizer = tiktoken.get_encoding('p50k_base')

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=20,
    length_function=lambda text: len(tokenizer.encode(text, disallowed_special=())),
    separators=["\n\n", "\n", " ", ""]
)

def get_loader_by_extension(extension):
    extension = extension.lower()
    if extension == ".txt":
        return TextLoader
    elif extension == ".pdf":
        return PyPDFLoader
    elif extension == ".docx":
        return UnstructuredWordDocumentLoader
    elif extension == ".ppt" or extension == ".pptx":
        return UnstructuredPowerPointLoader
    elif extension == ".html":
        return UnstructuredHTMLLoader
    elif extension == ".md":
        return UnstructuredMarkdownLoader
    elif extension == ".csv":
        return CSVLoader
    elif extension in {".jpg", ".jpeg", ".png", ".gif"}:
        return UnstructuredImageLoader
    else:
        raise ValueError(f"Unsupported file type: {extension}")


def process_uploaded_file(file: FileStorage, database: Database):
    # Need to make temp file because loaders need a temp file path in the project
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_file.name)
    extension = os.path.splitext(file.filename)[1]
    loader_cls = get_loader_by_extension(extension)
    loader = loader_cls(temp_file.name)
    documents = loader.load()
    os.unlink(temp_file.name)  # Delete the temporary file

    chunks = []
    for document in documents:
        texts = text_splitter.split_text(document.page_content)
        chunks.extend([{
            'text': texts[i],
            'chunk': i,
            'filename': file.filename
        } for i in range(len(texts))])

    database.insert_uploads_record(file.filename, len(chunks))
    
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        i_end = min(len(chunks), i + batch_size)
        meta_batch = chunks[i:i_end]

        data = {}
        for chunk in meta_batch:
            memory_entry = database.create_memory_entry([], chunk['text'], file.filename, source="uploaded")
            data.update(memory_entry)

        database.update_db(data)

    return {"success": "Successfully uploaded file!", "file_name": file.filename}
