# %% [markdown]
# # Multi-Agent LangGraph System - Refactored
# 
# This notebook demonstrates the refactored multi-agent system using modular code organization.

# %% [markdown]
# ## 1. Setup and Configuration

# %%
# Setup environment and imports
from src import (
    setup_environment,
    get_llm,
    create_rag_graph,
    create_research_graph,
    create_authoring_graph,
    create_supervisor_graph,
    create_chains,
    create_working_directory,
)
from src.utils import (
    load_loan_documents,
    load_complaints,
    create_text_splitter,
    create_vectorstore,
    get_nano_llm,
)
from langchain_core.messages import HumanMessage
import nest_asyncio

# Apply nest_asyncio for Jupyter compatibility
nest_asyncio.apply()

# Setup environment variables
setup_environment()

# %% [markdown]
# ## 2. Load and Process Documents

# %%
# Load loan knowledge documents
loan_knowledge_resources = load_loan_documents()
print(f"Loaded {len(loan_knowledge_resources)} loan documents")

# Create text splitter and split documents
text_splitter = create_text_splitter(chunk_size=750, chunk_overlap=0)
loan_knowledge_chunks = text_splitter.split_documents(loan_knowledge_resources)
print(f"Created {len(loan_knowledge_chunks)} chunks")

# Load complaints for reference
complaints = load_complaints()
print(f"Loaded {len(complaints)} complaints")

# %% [markdown]
# ## 3. Create Vector Stores

# %%
# Create vector stores
qdrant_vectorstore = create_vectorstore(loan_knowledge_chunks)
qdrant_retriever = qdrant_vectorstore.as_retriever()

qdrant_complaint_vectorstore = create_vectorstore(complaints)
qdrant_complaint_retriever = qdrant_complaint_vectorstore.as_retriever()

# %% [markdown]
# ## 4. Initialize Language Models

# %%
# Initialize language models
llm = get_llm("gpt-4o-mini")
nano_llm = get_nano_llm()

# %% [markdown]
# ## 5. Create RAG Graph

# %%
# Create and test RAG graph
rag_graph = create_rag_graph(qdrant_retriever, nano_llm)

# Test RAG graph
rag_result = rag_graph.invoke({"question": "What is the maximum loan amount?"})
print("RAG Response:", rag_result['response'])

# %% [markdown]
# ## 6. Create Team Graphs

# %%
# Create research team graph
research_graph = create_research_graph(llm, rag_graph)

# Create working directory for authoring team
working_directory = create_working_directory()
print(f"Working directory: {working_directory}")

# Create authoring team graph
authoring_graph = create_authoring_graph(llm, working_directory, qdrant_complaint_retriever)

# %% [markdown]
# ## 7. Create Chains and Supervisor

# %%
# Create chains from graphs
research_chain, authoring_chain = create_chains(research_graph, authoring_graph)

# Create main supervisor graph
compiled_super_graph = create_supervisor_graph(llm, research_chain, authoring_chain)

# %% [markdown]
# ## 8. Test Research Team

# %%
# Test research team
print("Testing Research Team:")
for s in research_chain.stream(
    "What is the maximum student loan in 2025?", {"recursion_limit": 100}
):
    if "__end__" not in s:
        print(s)
        print("---")

# %% [markdown]
# ## 9. Test Full Multi-Agent System

# %%
# Test the full multi-agent system
print("Testing Full Multi-Agent System:")
for s in compiled_super_graph.stream(
    {
        "messages": [
            HumanMessage(
                content="Write a customer assistance response on the positioning of Student Loans as it relates to low income students. First consult the research team. Then make sure you consult the response team, and check for copy editing and dopeness, and write the file to disk."
            )
        ],
    },
    {"recursion_limit": 30},
):
    if "__end__" not in s:
        print(s)
        print("---")

# %% [markdown]
# ## 10. Display Graph Visualizations

# %%
# Display graph visualizations
from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles

# Research graph
print("Research Team Graph:")
display(
    Image(
        research_graph.get_graph().draw_mermaid_png(
            curve_style=CurveStyle.LINEAR,
            node_colors=NodeStyles(first="#ffdfba", last="#baffc9", default="#fad7de"),
            wrap_label_n_words=9,
            output_file_path=None,
            draw_method=MermaidDrawMethod.PYPPETEER,
            background_color="white",
            padding=10,
        )
    )
)

# Authoring graph
print("\nAuthoring Team Graph:")
display(
    Image(
        authoring_graph.get_graph().draw_mermaid_png(
            curve_style=CurveStyle.LINEAR,
            node_colors=NodeStyles(first="#ffdfba", last="#baffc9", default="#fad7de"),
            wrap_label_n_words=9,
            output_file_path=None,
            draw_method=MermaidDrawMethod.PYPPETEER,
            background_color="white",
            padding=10,
        )
    )
)

# %% [markdown]
# ## 11. Check Generated Files

# %%
# List generated files
import os
print(f"Files in working directory ({working_directory}):")
for file in os.listdir(working_directory):
    print(f"  - {file}")
    
# Read and display one of the files if any exist
files = os.listdir(working_directory)
if files:
    sample_file = files[0]
    with open(working_directory / sample_file, 'r') as f:
        content = f.read()
    print(f"\nContent of {sample_file}:")
    print(content[:500] + "..." if len(content) > 500 else content)


