"""Research team agent configurations."""

import functools
from langchain_openai import ChatOpenAI
from .base import create_agent, create_team_supervisor
from ..tools.search import get_tavily_tool
from ..tools.retrieval import create_retrieve_information_tool
from ..nodes.common import agent_node


def create_search_agent(llm: ChatOpenAI):
    """Create the search agent with Tavily tool."""
    tavily_tool = get_tavily_tool()
    return create_agent(
        llm,
        [tavily_tool],
        "You are a research assistant who can search for up-to-date info using the tavily search engine.",
    )


def create_research_agent(llm: ChatOpenAI, rag_graph):
    """Create the research agent with retrieval tool."""
    retrieve_tool = create_retrieve_information_tool(rag_graph)
    return create_agent(
        llm,
        [retrieve_tool],
        "You are a research assistant who can provide specific information on the student loan policies",
    )


def create_research_supervisor(llm: ChatOpenAI, members: list = None):
    """Create the research team supervisor."""
    if members is None:
        members = ["Search", "LoanRetriever"]
    
    return create_team_supervisor(
        llm,
        (
            "You are a supervisor tasked with managing a conversation between the"
            " following workers:  Search, LoanRetriever. Given the following user request,"
            " determine the subject to be researched and respond with the worker to act next. Each worker will perform a"
            " task and respond with their results and status. "
            " You should never ask your team to do anything beyond research. They are not required to write content or posts."
            " You should only pass tasks to workers that are specifically research focused."
            " When finished, respond with FINISH."
        ),
        members,
    )


def create_research_nodes(llm: ChatOpenAI, rag_graph):
    """Create all research team nodes."""
    search_agent = create_search_agent(llm)
    research_agent = create_research_agent(llm, rag_graph)
    
    search_node = functools.partial(agent_node, agent=search_agent, name="Search")
    research_node = functools.partial(agent_node, agent=research_agent, name="LoanRetriever")
    
    return {
        "search_agent": search_agent,
        "research_agent": research_agent,
        "search_node": search_node,
        "research_node": research_node,
    }