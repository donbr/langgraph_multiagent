"""Configuration and setup utilities for the multi-agent system."""

import os
import tiktoken
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_openai import ChatOpenAI


def setup_environment():
    """Set up environment variables."""
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
    os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY", "")
    os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
    os.environ["LANGSMITH_PROJECT"] = "langgraph_multiagent"
    os.environ["LANGSMITH_TRACING"] = "true"


def tiktoken_len(text: str) -> int:
    """Calculate token length using tiktoken."""
    tokens = tiktoken.encoding_for_model("gpt-4o").encode(text)
    return len(tokens)


def create_text_splitter(chunk_size: int = 750, chunk_overlap: int = 0):
    """Create a text splitter with tiktoken length function."""
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=tiktoken_len,
    )


def load_loan_documents(data_dir: str = "data") -> list:
    """Load loan knowledge PDF documents."""
    directory_loader = DirectoryLoader(
        data_dir, 
        glob="**/*.pdf", 
        loader_cls=PyMuPDFLoader
    )
    return directory_loader.load()


def load_complaints(file_path: str = "data/complaints.csv") -> list:
    """Load complaint documents from CSV."""
    complaint_loader = CSVLoader(
        file_path,
        content_columns=[
            "Consumer complaint narrative", 
            "Company public response", 
            "Company response to consumer"
        ]
    )
    return complaint_loader.load()


def create_vectorstore(documents: list, embedding_model=None):
    """Create a Qdrant vectorstore from documents."""
    if embedding_model is None:
        embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    
    return Qdrant.from_documents(
        documents=documents,
        embedding=embedding_model,
        location=":memory:"
    )


def get_llm(model: str = "gpt-4o-mini"):
    """Get an OpenAI ChatModel instance."""
    return ChatOpenAI(model=model)


def get_nano_llm():
    """Get a nano version of the LLM for faster responses."""
    return ChatOpenAI(model="gpt-4o-mini")