# Multi-Agent LangGraph System - Source Code

**Purpose**: This is the technical architecture reference for the multi-agent LangGraph system. It provides detailed module documentation, implementation patterns, and serves as the authoritative source for code organization.

**Other Documentation**:
- 📚 [README.md](../README.md) - Start here for learning journey and setup instructions
- 🤖 [CLAUDE.md](../CLAUDE.md) - For developers using Claude Code (claude.ai/code)

This directory contains the refactored, modular implementation of the multi-agent LangGraph system. The code has been organized following LangGraph best practices and software engineering principles for maintainability, reusability, and type safety.

## References and Citations

This implementation is grounded in the following authoritative sources:

### LangGraph Official Documentation
- **Multi-Agent Patterns**: [LangGraph Multi-Agent Concepts](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) - Supervisor and hierarchical agent architectures
- **State Management**: [LangGraph State Schemas](https://langchain-ai.github.io/langgraph/concepts/low_level/) - TypedDict usage for graph state
- **Agent Creation**: [Building Agents](https://langchain-ai.github.io/langgraph/agents/overview/) - Prebuilt components and agent patterns
- **Graph Construction**: [StateGraph API](https://langchain-ai.github.io/langgraph/how-tos/graph-api/) - Graph building and edge definition patterns

### Software Engineering Best Practices
- **SOLID Principles**: [Real Python SOLID Guide](https://realpython.com/solid-principles-python/) - Single Responsibility and Dependency Inversion
- **Modular Architecture**: [Python Architecture Patterns](https://markparker5.medium.com/python-architecture-essentials-building-scalable-and-clean-application-for-juniors-41d59c29557c) - Clean code and modularity principles
- **Type Safety**: [Python Typing Best Practices](https://docs.python.org/3/library/typing.html) - TypedDict and type hint usage

### Industry Standards
- **API Design**: [LangChain Expression Language](https://python.langchain.com/docs/concepts/lcel/) - Composable chain patterns
- **Error Handling**: [LangGraph Error Patterns](https://langchain-ai.github.io/langgraph/troubleshooting/errors/) - Robust error handling strategies

## Directory Structure

```
src/
├── __init__.py              # Main package exports
├── agents/                  # Agent creation and configuration
│   ├── __init__.py
│   ├── base.py             # Base agent creation functions
│   ├── research.py         # Research team agents
│   └── authoring.py        # Authoring team agents
├── tools/                   # Tool implementations
│   ├── __init__.py
│   ├── retrieval.py        # RAG and retrieval tools
│   ├── document.py         # Document manipulation tools
│   └── search.py           # Search tools (Tavily)
├── states/                  # State type definitions
│   ├── __init__.py
│   └── types.py            # TypedDict state definitions
├── graphs/                  # Graph implementations
│   ├── __init__.py
│   ├── rag.py              # RAG graph
│   ├── research.py         # Research team graph
│   ├── authoring.py        # Authoring team graph
│   └── supervisor.py       # Main supervisor graph
├── nodes/                   # Common node functions
│   ├── __init__.py
│   └── common.py           # Shared node implementations
├── prompts/                 # Prompt templates
│   ├── __init__.py
│   └── templates.py        # ChatPromptTemplate definitions
└── utils/                   # Utility functions
    ├── __init__.py
    └── config.py            # Configuration and setup utilities

../content/data/             # Shared workspace architecture (external to src/)
└── <uuid>/                  # Session-isolated collaborative workspaces
    ├── *.md                # Production documents created by authoring team
    ├── *.txt               # Draft responses and notes
    └── outlines/           # Structured planning documents
```

## Key Features

### 1. **Modular Design**
- Each component has a single responsibility
- Clear separation of concerns
- Easy to test and maintain individual modules

### 2. **Type Safety**
- Comprehensive type hints throughout
- TypedDict state definitions
- Clear function signatures

### 3. **Reusability**
- Functions can be easily imported and reused
- Configurable parameters for different use cases
- Factory patterns for creating similar components

### 4. **Best Practices**
- Follows [LangGraph coding guidelines](https://langchain-ai.github.io/langgraph/how-tos/) for agent construction
- Implements [supervisor patterns](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) for multi-agent coordination
- Uses [TypedDict state schemas](https://langchain-ai.github.io/langgraph/concepts/low_level/) for type safety
- Applies [single responsibility principle](https://realpython.com/solid-principles-python/) for module organization

### 5. **Shared Workspace Architecture**
- **Multi-Agent Collaboration**: `content/data/` directory enables stateful collaboration between stateless LangGraph agents
- **Session Isolation**: UUID-based subdirectories prevent conflicts between concurrent workflows
- **Context Awareness**: `prelude()` function provides agents with awareness of teammate progress
- **Production Artifacts**: Stores high-quality finished documents as evidence of successful collaboration
- **State Persistence**: File system provides persistence layer for document creation workflows

## Usage

### Quick Start

```python
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

# Setup
setup_environment()
llm = get_llm()

# Create graphs
rag_graph = create_rag_graph(retriever, llm)
research_graph = create_research_graph(llm, rag_graph)
authoring_graph = create_authoring_graph(llm, working_directory)

# Create supervisor
research_chain, authoring_chain = create_chains(research_graph, authoring_graph)
supervisor_graph = create_supervisor_graph(llm, research_chain, authoring_chain)

# Run
result = supervisor_graph.invoke({"messages": [HumanMessage(content="Your query")]})
```

### Individual Components

```python
# Use individual tools
from src.tools import get_tavily_tool, create_retrieve_information_tool

# Use specific agents
from src.agents import create_research_nodes, create_authoring_nodes

# Use utilities
from src.utils import load_loan_documents, create_vectorstore
```

## Module Descriptions

### `agents/`
Contains agent creation functions organized by team:
- **base.py**: Core agent creation utilities (`create_agent`, `create_team_supervisor`) following [LangGraph agent patterns](https://langchain-ai.github.io/langgraph/agents/overview/)
- **research.py**: Research team specific agents (search, retrieval) implementing [tool-calling agents](https://langchain-ai.github.io/langgraph/concepts/tools/)
- **authoring.py**: Authoring team agents (writer, editor, note-taker) with [document manipulation tools](https://langchain-ai.github.io/langgraph/how-tos/tool-calling/)

### `tools/`
Tool implementations following [LangGraph tool patterns](https://langchain-ai.github.io/langgraph/concepts/tools/):
- **retrieval.py**: RAG-based information retrieval using [LangChain retrievers](https://python.langchain.com/docs/concepts/retrievers/)
- **document.py**: File manipulation tools with structured schemas
- **search.py**: Web search capabilities using [Tavily integration](https://python.langchain.com/docs/integrations/tools/tavily_search/)

### `graphs/`
Graph construction following [StateGraph patterns](https://langchain-ai.github.io/langgraph/how-tos/graph-api/):
- **rag.py**: Simple RAG retrieve-generate graph with [sequential processing](https://langchain-ai.github.io/langgraph/how-tos/graph-api/#sequences)
- **research.py**: Multi-agent research team using [supervisor architecture](https://langchain-ai.github.io/langgraph/concepts/multi_agent/)
- **authoring.py**: Document creation workflow with [conditional edges](https://langchain-ai.github.io/langgraph/how-tos/graph-api/#conditional-edges)
- **supervisor.py**: High-level orchestration implementing [hierarchical agents](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/)

### `states/`
Type-safe state definitions using [LangGraph state schemas](https://langchain-ai.github.io/langgraph/concepts/low_level/) with TypedDict patterns.

### `nodes/`
Common node functions following [node implementation patterns](https://langchain-ai.github.io/langgraph/how-tos/graph-api/#nodes) for reusability across graphs.

### `utils/`
Configuration and setup utilities following [environment best practices](https://python.langchain.com/docs/how_to/configure_runtime/) for LangChain applications.

## Benefits of This Structure

1. **Maintainability**: Clear organization following [clean code principles](https://arjancodes.com/blog/solid-principles-in-python-programming/) makes it easy to find and modify code
2. **Testability**: Individual modules can be unit tested in isolation, supporting [test-driven development](https://realpython.com/python-testing-101/)
3. **Reusability**: Components can be easily reused following [composition over inheritance](https://python-patterns.guide/gang-of-four/composition-over-inheritance/)
4. **Scalability**: Easy to add new agents, tools, or graph types following [open-closed principle](https://realpython.com/solid-principles-python/#open-closed-principle-ocp)
5. **Type Safety**: Comprehensive typing using [Python type hints](https://docs.python.org/3/library/typing.html) prevents runtime errors
6. **Documentation**: Self-documenting code structure with clear module boundaries

## Architecture Decisions

This implementation reflects current LangGraph best practices as of 2024-2025:

### Multi-Agent Architecture
- **Supervisor Pattern**: Based on [LangGraph supervisor examples](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/) for coordinating specialized agents
- **Hierarchical Teams**: Implements [hierarchical agent teams](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/) for complex workflows
- **State Management**: Uses [TypedDict schemas](https://langchain-ai.github.io/langgraph/concepts/low_level/) for type-safe state passing

### Design Patterns
- **Factory Pattern**: For creating configurable agents and graphs
- **Strategy Pattern**: For different agent behaviors within teams
- **Command Pattern**: Through LangGraph's message passing architecture

## Migration from Notebook

The original notebook code has been refactored into this modular structure while maintaining the same functionality. This follows [software refactoring best practices](https://refactoring.guru/refactoring) for improving code organization without changing behavior.

The new `multiagent_refactored.ipynb` demonstrates how to use the modular components, showcasing the improved developer experience and code clarity.