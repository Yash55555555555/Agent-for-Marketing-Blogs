## we will keep all the functions here which will be used in multiple places

from langchain.document_loaders import PyPDFLoader , DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from typing import List
from langchain.schema import Document

# extract data from the pdf file

def load_pdf_file(data):
    loader = DirectoryLoader(
        data,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()
    return documents

# document minimal function
def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    '''
    given a list of documents objects  , return a list of documents  objects containing only source and page content.
    '''
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source") 
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata = {"source": src}
        )
    )
    return minimal_docs


# split the documents into smallert chunks

def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=20
    )
    texts_chunks = text_splitter.split_documents(minimal_docs)
    return texts_chunks

# download the embedding model from hugging face
def download_embeddings():
    '''
    download and return the embedding model
    '''
    model_name = "sentence-transformers/all-MiniLM-L6-v2"   # vector dimension 384
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name
    )
    return embeddings

