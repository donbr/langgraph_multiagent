"""Common node functions for the multi-agent system."""

from pathlib import Path
from typing import Dict, List
from langchain_core.messages import HumanMessage, BaseMessage
from ..states.types import DocWritingState, SupervisorState


def agent_node(state: dict, agent, name: str) -> dict:
    """Generic agent node that invokes an agent and returns its message."""
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}


def prelude(state: DocWritingState, working_directory: Path) -> DocWritingState:
    """Prepare state with current file information."""
    written_files = []
    if not working_directory.exists():
        working_directory.mkdir()
    try:
        written_files = [
            f.relative_to(working_directory) for f in working_directory.rglob("*")
        ]
    except:
        pass
    if not written_files:
        return {**state, "current_files": "No files written."}
    return {
        **state,
        "current_files": "\nBelow are files your team has written to the directory:\n"
        + "\n".join([f" - {f}" for f in written_files]),
    }


def enter_chain(message: str, members: List[str] = None) -> dict:
    """Entry point for chain execution."""
    results = {
        "messages": [HumanMessage(content=message)],
    }
    if members:
        results["team_members"] = ", ".join(members)
    return results


def get_last_message(state: SupervisorState) -> str:
    """Extract the last message content from state."""
    return state["messages"][-1].content


def join_graph(response: dict) -> dict:
    """Join graph results by extracting the last message."""
    return {"messages": [response["messages"][-1]]}