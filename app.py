from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# LangChain and Pinecone imports

# Updated imports for LangChain v0.3.x and Pinecone
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

app = FastAPI()
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

class QueryRequest(BaseModel):
	query: str

# --- RAG Setup (run once at startup) ---
DATA_DIR = "data/"
INDEX_NAME = "langchain-research"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Load and process documents
def load_pdf_file(data):
	loader = DirectoryLoader(
		data,
		glob="*.pdf",
		loader_cls=PyPDFLoader
	)
	documents = loader.load()
	return documents

def filter_to_minimal_docs(docs):
	from langchain_core.documents import Document
	minimal_docs = []
	for doc in docs:
		src = doc.metadata.get("source")
		minimal_docs.append(
			Document(
				page_content=doc.page_content,
				metadata={"source": src}
			)
		)
	return minimal_docs

def text_split(minimal_docs):
	text_splitter = RecursiveCharacterTextSplitter(
		chunk_size=300,
		chunk_overlap=20
	)
	texts_chunks = text_splitter.split_documents(minimal_docs)
	return texts_chunks

# Embedding
embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# Load environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")




# Pinecone setup (latest API)
pc = Pinecone(api_key=PINECONE_API_KEY)
if INDEX_NAME not in pc.list_indexes().names():
	pc.create_index(
		name=INDEX_NAME,
		dimension=384,
		metric="cosine"
	)
index = pc.Index(INDEX_NAME)

# Load and process data
extracted_data = load_pdf_file(DATA_DIR)
minimal_docs = filter_to_minimal_docs(extracted_data)
texts_chunks = text_split(minimal_docs)

# Store vectors
docsearch = PineconeVectorStore.from_documents(
	documents=texts_chunks,
	embedding=embedding,
	index_name=INDEX_NAME
)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":4})

# LLM setup
llm = ChatOpenAI(
	api_key=OPENROUTER_API_KEY,
	base_url="https://openrouter.ai/api/v1",
	model="mistralai/mistral-7b-instruct",
	temperature=0.5
)

system_prompt = (
	"you are an helpful assistant for the task of marketing blogs based on the user query."
	"if you think the answer is not good as per the question from the retrieved context, you can generate the answer on your own so that user can get the best answer."
	"use four sentences maximum to answer the query."
	"\n\n"
	"{context}"
)
prompt = ChatPromptTemplate.from_messages([
	("system", system_prompt),
	("human", "{input}")
])
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# --- API Endpoint ---
@app.post("/api/query")
async def answer_query(request: QueryRequest):
	user_query = request.query
	try:
		response = rag_chain.invoke({"input": user_query})
		answer = response.get("answer", "No answer generated.")
		return {"response": answer}
	except Exception as e:
		return {"response": f"Error: {str(e)}"}
