"""RAG graph implementation."""

from langgraph.graph import START, StateGraph
from langchain_core.output_parsers import StrOutputParser
from ..states.types import State
from ..prompts.templates import get_rag_prompt


def retrieve(state: State, retriever) -> State:
    """Retrieve documents based on the question."""
    retrieved_docs = retriever.invoke(state["question"])
    return {"context": retrieved_docs}


def generate(state: State, llm) -> State:
    """Generate response using retrieved context."""
    chat_prompt = get_rag_prompt()
    generator_chain = chat_prompt | llm | StrOutputParser()
    response = generator_chain.invoke({"query": state["question"], "context": state["context"]})
    return {"response": response}


def create_rag_graph(retriever, llm):
    """Create and compile the RAG graph.
    
    Args:
        retriever: The retriever to use for document lookup
        llm: The language model to use for generation
        
    Returns:
        Compiled RAG graph
    """
    # Create retrieve and generate functions with bound parameters
    retrieve_fn = lambda state: retrieve(state, retriever)
    generate_fn = lambda state: generate(state, llm)
    
    # Build the graph
    graph_builder = StateGraph(State)
    graph_builder = graph_builder.add_sequence([("retrieve", retrieve_fn), ("generate", generate_fn)])
    graph_builder.add_edge(START, "retrieve")
    
    return graph_builder.compile()