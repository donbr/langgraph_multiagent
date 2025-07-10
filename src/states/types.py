"""State type definitions for LangGraph multi-agent system."""

from typing import Annotated, List
from typing_extensions import TypedDict
import operator
from langchain_core.messages import BaseMessage
from langchain_core.documents import Document


class State(TypedDict):
    """Base state for RAG operations."""
    question: str
    context: list[Document]
    response: str


class ResearchTeamState(TypedDict):
    """State for research team operations."""
    messages: Annotated[List[BaseMessage], operator.add]
    team_members: List[str]
    next: str


class DocWritingState(TypedDict):
    """State for document writing team operations."""
    messages: Annotated[List[BaseMessage], operator.add]
    team_members: str
    next: str
    current_files: str


class SupervisorState(TypedDict):
    """State for main supervisor orchestration."""
    messages: Annotated[List[BaseMessage], operator.add]
    next: str