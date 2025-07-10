# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-agent LangGraph system for customer assistance responses about student loan policies. The system uses a hierarchical multi-agent architecture with specialized teams for research and document authoring, coordinated by a supervisor agent.

**Important**: This codebase follows the **parsimony principle** - only refactor or modify code when there is clear, demonstrable value. The existing architecture already follows LangGraph best practices and should not be over-engineered.

## Architecture

### Core Flow
The system operates through a three-tier architecture:
1. **RAG Layer**: Basic retrieval-augmented generation for document lookup
2. **Specialized Teams**: Research team (web search + document retrieval) and Authoring team (document creation + editing)
3. **Supervisor Orchestration**: Meta-supervisor coordinates between teams based on task requirements

> 📊 **Visual Guide**: See the [interactive architecture diagram](https://app.devin.ai/wiki/donbr/langgraph_multiagent#architecture) for a complete visualization of the three-tier system and message flow.

### Key Architectural Patterns
- **State Management**: Each graph type has its own TypedDict state (`State`, `ResearchTeamState`, `DocWritingState`, `SupervisorState`)
- **Agent Composition**: Agents are created using factory functions with LLM + tools + system prompts
- **Graph Chaining**: Subgraphs are connected through entry points and message passing
- **Tool Binding**: Tools are bound to specific agents based on their specialized functions

## Common Development Commands

### Environment Setup
```bash
# Install dependencies (requires Python 3.11)
uv sync

# Set required environment variables
export OPENAI_API_KEY="your_key"
export TAVILY_API_KEY="your_key" 
export LANGSMITH_API_KEY="your_key"
```

### Running the System
```bash
# Start Jupyter for notebook development
jupyter lab

# Run the refactored notebook
jupyter lab multiagent_refactored.ipynb
```

### Working with the Modular Code
```python
# Import the main system components
from src import (
    setup_environment,
    create_rag_graph,
    create_research_graph, 
    create_authoring_graph,
    create_supervisor_graph
)

# Setup and run end-to-end
setup_environment()
llm = get_llm()
rag_graph = create_rag_graph(retriever, llm)
# ... build complete system
```

## Code Organization Principles

### Module Hierarchy
- `src/agents/`: Agent creation functions, organized by team specialization
- `src/graphs/`: Graph construction logic, each module handles one graph type
- `src/tools/`: Tool implementations, grouped by functionality (search, retrieval, document manipulation)
- `src/states/`: TypedDict definitions for type-safe state management
- `src/nodes/`: Reusable node functions that work across different graphs
- `src/utils/`: Configuration and utility functions for setup and data loading

### State Flow Architecture
State flows unidirectionally through the system:
1. **Supervisor State** (`SupervisorState`): High-level message coordination
2. **Team States** (`ResearchTeamState`, `DocWritingState`): Team-specific state management with member tracking
3. **Base State** (`State`): Simple RAG operations with question/context/response

> 🔄 **Visual Guide**: View the [state flow diagram](https://app.devin.ai/wiki/donbr/langgraph_multiagent#state-flow) to see how data moves between different graph states.

### Agent Creation Pattern
All agents follow the same creation pattern:
1. Create agent using `create_agent(llm, tools, system_prompt)`
2. Wrap agent in node function using `functools.partial(agent_node, agent=agent, name="Name")`
3. Add to graph with appropriate edges and conditional routing

## Multi-Agent Collaboration Architecture

### Stateful Collaboration Pattern
The system implements a sophisticated pattern for enabling stateful collaboration between stateless LangGraph agents:

**1. Document Tools Integration**
- `create_document_tools()` provides file system operations (create_outline, write_document, edit_document, read_document)
- Each agent receives tools scoped to their specific working directory
- Tools enable persistent state across agent invocations

**2. Context Awareness System**
- `prelude()` function scans the working directory before each agent invocation
- Injects current file listing into agent prompts: "Below are files your team has written to the directory"
- Enables agents to understand what teammates have accomplished

**3. Collaborative Workflow Pattern**
```
NoteTaker → creates outline and research notes
DocWriter → reads outline, creates initial document  
CopyEditor → reads document, fixes grammar/tone
DopenessEditor → reads document, adds engaging elements
```

> 🤝 **Visual Guide**: See the [agent collaboration sequence diagram](https://app.devin.ai/wiki/donbr/langgraph_multiagent#collaboration) showing how agents work together through the shared workspace.

**4. Production Quality Validation**
- Example outputs demonstrate genuine multi-agent collaboration
- Documents show evidence of each agent's specialization
- Final deliverables are production-ready customer assistance responses

### Architectural Benefits
- **Scalable**: UUID isolation enables concurrent multi-user workflows
- **Robust**: File system persistence survives agent failures
- **Traceable**: Complete audit trail of collaborative document creation
- **Extensible**: Easy to add new agent types with document tools

## Data Flow

### Document Processing Pipeline
1. **Load**: PDF documents and CSV complaints using utility functions
2. **Chunk**: Documents split using tiktoken-based text splitter  
3. **Embed**: Create vector stores using OpenAI embeddings
4. **Retrieve**: Multiple retrievers for different document types

### Multi-Agent Execution Flow
1. **Entry**: Supervisor receives user message
2. **Route**: Supervisor decides which team to invoke (Research/Response)
3. **Execute**: Team supervisor coordinates team members
4. **Aggregate**: Results flow back to main supervisor
5. **Output**: Final response or handoff to next team

> 🎯 **Visual Guide**: Explore the [execution flow visualization](https://app.devin.ai/wiki/donbr/langgraph_multiagent#execution-flow) to see conditional routing and error handling in action.

## Key Configuration

### Environment Variables
- `OPENAI_API_KEY`: Required for LLM operations
- `TAVILY_API_KEY`: Required for web search functionality
- `LANGSMITH_API_KEY`: Optional for tracing
- `LANGSMITH_PROJECT`: Set to "langgraph_multiagent"

### Model Configuration
- Primary LLM: `gpt-4o-mini` for agents
- RAG LLM: `gpt-4o-mini` for faster retrieval responses  
- Embeddings: `text-embedding-3-small` for vector operations

### Known Issues and Deprecations
- `bind_functions` is deprecated but still functional - avoid changing unless breaking
- `TavilySearchResults` has import location changes but works with fallback
- Lambda naming conflicts in graphs resolved using tuple format: `("name", function)`

### Shared Workspace Architecture (`content/data/`)

The `content/data/` directory represents a **fundamental architectural component** for multi-agent collaborative document creation, not merely a temporary working directory.

**Architectural Purpose:**
- **Shared Workspace Pattern**: Provides file system-based shared memory where multiple agents (DocWriter, NoteTaker, CopyEditor, DopenessEditor) collaborate on the same documents
- **State Persistence Layer**: Solves the stateless agent collaboration problem by maintaining work products between agent invocations  
- **Context Awareness System**: The `prelude()` function scans the directory and injects current file information into agent prompts, enabling agents to understand teammate progress
- **Session Isolation**: UUID-based subdirectories (e.g., `775c351a/`) prevent conflicts between concurrent user workflows
- **Production Artifact Repository**: Stores high-quality finished deliverables as evidence of successful multi-agent collaboration

**Critical for Production**: This pattern enables stateful collaboration between stateless LangGraph agents, making production-quality document generation workflows possible.

## Development Guidelines

### Refactoring Philosophy
**Follow the parsimony principle**: Only make changes that provide clear, measurable value. The current architecture already follows LangGraph best practices from official documentation:
- [Multi-Agent Patterns](https://langchain-ai.github.io/langgraph/concepts/multi_agent/)
- [State Management](https://langchain-ai.github.io/langgraph/concepts/low_level/)
- [Agent Creation](https://langchain-ai.github.io/langgraph/agents/overview/)

### When NOT to Refactor
- Working deprecation warnings (functions still operate correctly)
- Existing patterns that follow official LangGraph examples
- Code that successfully implements documented patterns
- Architecture that already demonstrates clean separation of concerns

### Extending the System

#### Adding New Agents
1. Create agent function in appropriate `src/agents/` module
2. Define tools in `src/tools/` if needed
3. Add to team supervisor's member list
4. Update graph construction in `src/graphs/`

#### Adding New Tools
1. Implement tool function in `src/tools/`
2. Add to appropriate agent creation function
3. Update tool exports in `__init__.py`

#### Adding New Graph Types
1. Define new state type in `src/states/types.py`
2. Create graph construction function in `src/graphs/`
3. Add to main exports in `src/__init__.py`

## Notebook Usage Patterns

The system supports both monolithic notebook usage (original) and modular development (refactored). The refactored approach imports clean functions from `src/` modules, while the original notebooks contain all logic inline.

For development, use `multiagent_refactored.ipynb` which demonstrates the modular architecture and cleaner separation of concerns.

## Architecture Validation

This implementation has been validated against authoritative sources:
- **LangGraph Official Documentation**: All patterns follow documented examples
- **Software Engineering Best Practices**: SOLID principles and clean architecture
- **Industry Standards**: Type safety with TypedDict, modular design patterns

See `src/README.md` for comprehensive citations and references supporting architectural decisions.

## Testing and Validation

### Quick Testing
```bash
# Run simplified demo
python demo_refactored.py

# Test specific components
python -c "from src import create_rag_graph; print('Import successful')"
```

### Common Issues
- **Lambda naming conflicts**: Use tuple format `("name", function)` in graph sequences
- **None chain errors**: Check authoring_graph exists before creating chains
- **Import errors**: Verify all `__init__.py` files have proper exports

## content/data Management

### Production Workspace Management
**⚠️ Important**: The `content/data/` directory contains production outputs from multi-agent workflows and should be managed carefully.

### Best Practices
- **Session Isolation**: Each workflow automatically creates UUID-based subdirectories
- **Cleanup Strategy**: Implement periodic cleanup of old session directories
- **Backup Considerations**: Production documents may need preservation for compliance
- **Concurrent Access**: Multiple users can run workflows simultaneously due to UUID isolation

### Directory Structure Understanding
```bash
content/data/
├── 775c351a/           # Session UUID from previous run
│   └── Customer_Assistance_Student_Loans_Response.md
├── 1d7b4d9f/           # Another session UUID  
│   └── Student_Loans_Low_Income_Students_Response.txt
└── <new-uuid>/         # New session created automatically
```

### Git Management
- `content/` is automatically ignored by git (included in `.gitignore`)
- Production data is not versioned to protect user privacy
- Sample outputs are preserved in this repository for demonstration purposes

### Troubleshooting Workspace Issues
- **Permission Errors**: Ensure write permissions to `./content/data/`
- **Disk Space**: Monitor usage as each session creates new documents
- **Path Resolution**: Working directory creation uses relative paths from execution location

## Visual Documentation & Interactive Resources

For a deeper understanding of this system through visual representations, explore the [DeepWiki documentation portal](https://app.devin.ai/wiki/donbr/langgraph_multiagent) which provides:

### 🏗️ Architecture Diagrams
- **[System Architecture](https://app.devin.ai/wiki/donbr/langgraph_multiagent#architecture)**: Interactive visualization of the three-tier architecture and component relationships
- **[State Management](https://app.devin.ai/wiki/donbr/langgraph_multiagent#state-flow)**: Visual representation of state flow between different graph types
- **[Tool Binding Matrix](https://app.devin.ai/wiki/donbr/langgraph_multiagent#tools)**: See which tools are available to which agents

### 📊 Performance & Analysis
- **[Performance Benchmarks](https://app.devin.ai/wiki/donbr/langgraph_multiagent#performance)**: Detailed analysis comparing retrieval strategies
- **[Agent Invocation Patterns](https://app.devin.ai/wiki/donbr/langgraph_multiagent#patterns)**: Visualize how agents are called in different scenarios
- **[Resource Utilization](https://app.devin.ai/wiki/donbr/langgraph_multiagent#resources)**: Understand system resource usage

### 🔧 Implementation Details
- **[Collaboration Workflows](https://app.devin.ai/wiki/donbr/langgraph_multiagent#collaboration)**: Sequence diagrams showing agent teamwork
- **[Error Recovery Flows](https://app.devin.ai/wiki/donbr/langgraph_multiagent#error-handling)**: Visual guide to system resilience
- **[LangSmith Trace Examples](https://app.devin.ai/wiki/donbr/langgraph_multiagent#traces)**: Real execution traces for debugging

### 🚀 Quick Visual Reference

| Concept | Visual Resource | Use Case |
|---------|----------------|----------|
| Agent Hierarchy | [Architecture Diagram](https://app.devin.ai/wiki/donbr/langgraph_multiagent#architecture) | Understanding system structure |
| State Flow | [State Machine Diagram](https://app.devin.ai/wiki/donbr/langgraph_multiagent#state-flow) | Debugging state transitions |
| Agent Collaboration | [Sequence Diagrams](https://app.devin.ai/wiki/donbr/langgraph_multiagent#collaboration) | Optimizing workflows |
| Performance | [Benchmark Charts](https://app.devin.ai/wiki/donbr/langgraph_multiagent#performance) | System optimization |

These visual resources complement the text documentation and provide interactive ways to explore the system's complexity.