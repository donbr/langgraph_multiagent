"""Research team graph implementation."""

from langgraph.graph import END, StateGraph
from ..states.types import ResearchTeamState
from ..agents.research import create_research_nodes, create_research_supervisor


def create_research_graph(llm, rag_graph):
    """Create and compile the research team graph.
    
    Args:
        llm: The language model to use
        rag_graph: The compiled RAG graph for retrieval
        
    Returns:
        Compiled research team graph
    """
    # Create nodes
    nodes = create_research_nodes(llm, rag_graph)
    supervisor_agent = create_research_supervisor(llm)
    
    # Build graph
    research_graph = StateGraph(ResearchTeamState)
    
    # Add nodes
    research_graph.add_node("Search", nodes["search_node"])
    research_graph.add_node("LoanRetriever", nodes["research_node"])
    research_graph.add_node("supervisor", supervisor_agent)
    
    # Add edges
    research_graph.add_edge("Search", "supervisor")
    research_graph.add_edge("LoanRetriever", "supervisor")
    
    # Add conditional edges
    research_graph.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {"Search": "Search", "LoanRetriever": "LoanRetriever", "FINISH": END},
    )
    
    # Set entry point
    research_graph.set_entry_point("supervisor")
    
    return research_graph.compile()