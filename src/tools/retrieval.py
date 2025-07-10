"""Retrieval tools for RAG operations."""

from typing import Annotated
from langchain_core.tools import tool


def create_retrieve_information_tool(rag_graph):
    """Create a retrieval tool that uses the RAG graph.
    
    Args:
        rag_graph: The compiled RAG graph to use for retrieval
        
    Returns:
        A tool function for retrieving information
    """
    @tool
    def retrieve_information(
        query: Annotated[str, "query to ask the retrieve information tool"]
    ):
        """Use Retrieval Augmented Generation to retrieve information about student loan policies"""
        return rag_graph.invoke({"question": query})
    
    return retrieve_information