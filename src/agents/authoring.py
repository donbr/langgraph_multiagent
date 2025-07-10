"""Authoring team agent configurations."""

import functools
from pathlib import Path
from langchain_openai import ChatOpenAI
from .base import create_agent, create_team_supervisor
from ..tools.document import create_document_tools
from ..nodes.common import agent_node, prelude


def create_doc_writer_agent(llm: ChatOpenAI, working_directory: Path):
    """Create the document writer agent."""
    doc_tools = create_document_tools(working_directory)
    tools = [doc_tools["write_document"], doc_tools["edit_document"], doc_tools["read_document"]]
    
    return create_agent(
        llm,
        tools,
        (
            "You are an expert writing customer assistance responses.\n"
            "Below are files currently in your directory:\n{current_files}"
        ),
    )


def create_note_taking_agent(llm: ChatOpenAI, working_directory: Path, complaint_retriever=None):
    """Create the note taking agent."""
    doc_tools = create_document_tools(working_directory, complaint_retriever)
    tools = [doc_tools["create_outline"], doc_tools["read_document"], doc_tools["reference_previous_responses"]]
    
    return create_agent(
        llm,
        tools,
        (
            "You are an expert senior researcher tasked with writing a customer assistance outline and"
            " taking notes to craft a customer assistance response.\n{current_files}"
        ),
    )


def create_copy_editor_agent(llm: ChatOpenAI, working_directory: Path):
    """Create the copy editor agent."""
    doc_tools = create_document_tools(working_directory)
    tools = [doc_tools["write_document"], doc_tools["edit_document"], doc_tools["read_document"]]
    
    return create_agent(
        llm,
        tools,
        (
            "You are an expert copy editor who focuses on fixing grammar, spelling, and tone issues\n"
            "Below are files currently in your directory:\n{current_files}"
        ),
    )


def create_dopeness_editor_agent(llm: ChatOpenAI, working_directory: Path):
    """Create the dopeness editor agent."""
    doc_tools = create_document_tools(working_directory)
    tools = [doc_tools["write_document"], doc_tools["edit_document"], doc_tools["read_document"]]
    
    return create_agent(
        llm,
        tools,
        (
            "You are an expert in dopeness, litness, coolness, etc - you edit the document to make sure it's dope. "
            "Make sure to use a number of emojis."
            "Below are files currently in your directory:\n{current_files}"
        ),
    )


def create_doc_writing_supervisor(llm: ChatOpenAI, members: list = None):
    """Create the document writing team supervisor."""
    if members is None:
        members = ["DocWriter", "NoteTaker", "DopenessEditor", "CopyEditor"]
    
    return create_team_supervisor(
        llm,
        (
            "You are a supervisor tasked with managing a conversation between the"
            " following workers: {team_members}. You should always verify the technical"
            " contents after any edits are made. "
            "Given the following user request,"
            " respond with the worker to act next. Each worker will perform a"
            " task and respond with their results and status. When each team is finished,"
            " you must respond with FINISH."
        ),
        members,
    )


def create_authoring_nodes(llm: ChatOpenAI, working_directory: Path, complaint_retriever=None):
    """Create all authoring team nodes with prelude context."""
    # Create agents
    doc_writer_agent = create_doc_writer_agent(llm, working_directory)
    note_taking_agent = create_note_taking_agent(llm, working_directory, complaint_retriever)
    copy_editor_agent = create_copy_editor_agent(llm, working_directory)
    dopeness_editor_agent = create_dopeness_editor_agent(llm, working_directory)
    
    # Wrap agents with prelude
    prelude_fn = functools.partial(prelude, working_directory=working_directory)
    
    context_aware_doc_writer = prelude_fn | doc_writer_agent
    context_aware_note_taker = prelude_fn | note_taking_agent
    context_aware_copy_editor = prelude_fn | copy_editor_agent
    context_aware_dopeness_editor = prelude_fn | dopeness_editor_agent
    
    # Create nodes
    doc_writing_node = functools.partial(agent_node, agent=context_aware_doc_writer, name="DocWriter")
    note_taking_node = functools.partial(agent_node, agent=context_aware_note_taker, name="NoteTaker")
    copy_editing_node = functools.partial(agent_node, agent=context_aware_copy_editor, name="CopyEditor")
    dopeness_node = functools.partial(agent_node, agent=context_aware_dopeness_editor, name="DopenessEditor")
    
    return {
        "doc_writer_agent": doc_writer_agent,
        "note_taking_agent": note_taking_agent,
        "copy_editor_agent": copy_editor_agent,
        "dopeness_editor_agent": dopeness_editor_agent,
        "doc_writing_node": doc_writing_node,
        "note_taking_node": note_taking_node,
        "copy_editing_node": copy_editing_node,
        "dopeness_node": dopeness_node,
    }