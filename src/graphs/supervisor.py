"""Main supervisor graph implementation."""

import functools
from langgraph.graph import END, StateGraph
from ..states.types import SupervisorState
from ..agents.base import create_team_supervisor
from ..nodes.common import get_last_message, join_graph, enter_chain


def create_supervisor_graph(llm, research_chain, authoring_chain):
    """Create and compile the main supervisor graph.
    
    Args:
        llm: The language model to use
        research_chain: Compiled research team chain
        authoring_chain: Compiled authoring team chain
        
    Returns:
        Compiled supervisor graph
    """
    # Create supervisor
    supervisor_node = create_team_supervisor(
        llm,
        "You are a supervisor tasked with managing a conversation between the"
        " following teams: {team_members}. Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status. When all workers are finished,"
        " you must respond with FINISH.",
        ["Research team", "Response team"],
    )
    
    # Build graph
    super_graph = StateGraph(SupervisorState)
    
    # Add nodes
    super_graph.add_node("Research team", get_last_message | research_chain | join_graph)
    super_graph.add_node("Response team", get_last_message | authoring_chain | join_graph)
    super_graph.add_node("supervisor", supervisor_node)
    
    # Add edges
    super_graph.add_edge("Research team", "supervisor")
    super_graph.add_edge("Response team", "supervisor")
    
    # Add conditional edges
    super_graph.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {
            "Response team": "Response team",
            "Research team": "Research team",
            "FINISH": END,
        },
    )
    
    # Set entry point
    super_graph.set_entry_point("supervisor")
    
    return super_graph.compile()


def create_chains(research_graph, authoring_graph):
    """Create chains from graphs with enter_chain entry points.
    
    Args:
        research_graph: Compiled research graph
        authoring_graph: Compiled authoring graph (can be None)
        
    Returns:
        Tuple of (research_chain, authoring_chain)
    """
    # Create research chain
    research_chain = enter_chain | research_graph if research_graph else None
    
    # Create authoring chain with members
    authoring_chain = None
    if authoring_graph:
        authoring_nodes = ["DocWriter", "NoteTaker", "CopyEditor", "DopenessEditor", "supervisor"]
        authoring_chain = functools.partial(enter_chain, members=authoring_nodes) | authoring_graph
    
    return research_chain, authoring_chain