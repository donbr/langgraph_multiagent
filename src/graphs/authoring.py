"""Authoring team graph implementation."""

from pathlib import Path
from langgraph.graph import END, StateGraph
from ..states.types import DocWritingState
from ..agents.authoring import create_authoring_nodes, create_doc_writing_supervisor


def create_authoring_graph(llm, working_directory: Path, complaint_retriever=None):
    """Create and compile the authoring team graph.
    
    Args:
        llm: The language model to use
        working_directory: Directory for document storage
        complaint_retriever: Optional retriever for previous responses
        
    Returns:
        Compiled authoring team graph
    """
    # Create nodes
    nodes = create_authoring_nodes(llm, working_directory, complaint_retriever)
    supervisor = create_doc_writing_supervisor(llm)
    
    # Build graph
    authoring_graph = StateGraph(DocWritingState)
    
    # Add nodes
    authoring_graph.add_node("DocWriter", nodes["doc_writing_node"])
    authoring_graph.add_node("NoteTaker", nodes["note_taking_node"])
    authoring_graph.add_node("CopyEditor", nodes["copy_editing_node"])
    authoring_graph.add_node("DopenessEditor", nodes["dopeness_node"])
    authoring_graph.add_node("supervisor", supervisor)
    
    # Add edges
    authoring_graph.add_edge("DocWriter", "supervisor")
    authoring_graph.add_edge("NoteTaker", "supervisor")
    authoring_graph.add_edge("CopyEditor", "supervisor")
    authoring_graph.add_edge("DopenessEditor", "supervisor")
    
    # Add conditional edges
    authoring_graph.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {
            "DocWriter": "DocWriter",
            "NoteTaker": "NoteTaker",
            "CopyEditor": "CopyEditor",
            "DopenessEditor": "DopenessEditor",
            "FINISH": END,
        },
    )
    
    # Set entry point
    authoring_graph.set_entry_point("supervisor")
    
    return authoring_graph.compile()