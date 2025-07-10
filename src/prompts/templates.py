"""Prompt templates for the multi-agent system."""

from langchain_core.prompts import ChatPromptTemplate


# RAG prompt template
HUMAN_TEMPLATE = """
#CONTEXT:
{context}

QUERY:
{query}

Use the provide context to answer the provided user query. Only use the provided context to answer the query. If you do not know the answer, or it's not contained in the provided context respond with "I don't know"
"""

def get_rag_prompt() -> ChatPromptTemplate:
    """Get the RAG chat prompt template."""
    return ChatPromptTemplate.from_messages([
        ("human", HUMAN_TEMPLATE)
    ])