# Multi-Agent AI Systems: From Simple RAG to Team Coordination

## TLDR - Quick Run

**Just want to run the code?** Here's how:

```bash
# 1. Install dependencies (requires Python 3.11+)
uv sync

# 2. Set your API keys
export OPENAI_API_KEY="your-openai-key"
export TAVILY_API_KEY="your-tavily-key"
export LANGSMITH_API_KEY="your-langsmith-key"  # Optional but recommended

# 3. Run it!
jupyter lab multiagent_refactored.ipynb
# OR run the demo script
python demo_refactored.py
```

**Get API Keys:**
- [OpenAI](https://platform.openai.com/api-keys) (free tier works)
- [Tavily](https://tavily.com/) (free tier works)  
- [LangSmith](https://smith.langchain.com/) (optional - enables agent tracing)

**Troubleshooting:** If `uv` command not found, install it first: `curl -LsSf https://astral.sh/uv/install.sh | sh`

---

## About This Project

> **Why This Matters**: Imagine having a team of AI assistants that can research, write, and edit documents together - just like human teams, but faster and more consistent. This project teaches you to build exactly that using LangGraph.

## What You'll Build

By the end of this journey, you'll create an AI system where:
- 🔍 **Research agents** gather information from the web and documents
- ✍️ **Writing agents** create structured content 
- 📝 **Editor agents** refine and polish the output
- 🎯 **Supervisor agents** coordinate the entire workflow

**Real Example**: Ask your system "Write a guide about student loans for low-income students" and watch multiple AI agents collaborate to research, write, and edit a comprehensive response.

## Your Learning Path

### 🌱 Phase 1: Foundation (30-45 minutes)
**Goal**: Understand what multi-agent systems are and why they're powerful

**Start Here**: `multiagent_refactored.ipynb`

**You'll Learn**:
- What is RAG (Retrieval-Augmented Generation)?
- How do AI agents make decisions?
- Why use multiple agents instead of one?

**Success Check**: ✅ You can explain the difference between a single AI model and a multi-agent system

### 🏗️ Phase 2: Modular Architecture (1-2 hours)
**Goal**: Build systems using reusable components

**Work With**: `multiagent_refactored.ipynb` + `src/` directory

**You'll Learn**:
- How to organize code for maintainability
- Creating agents with specific roles
- Building workflows as graphs

**Success Check**: ✅ You can modify an agent's behavior by changing its tools or prompt

### 🚀 Phase 3: Advanced Coordination (2-3 hours)
**Goal**: Master complex agent interactions and real-world patterns

**Explore**: `src/graphs/supervisor.py`, `content/data/` workspace

**You'll Learn**:
- Hierarchical team management
- Shared workspace collaboration
- Error handling and recovery

**Success Check**: ✅ You can add a new agent type and integrate it into the workflow

### 🔍 Why LangSmith? (Highly Recommended)

[LangSmith](https://smith.langchain.com/) is like having X-ray vision into your multi-agent system. It shows you:

- **Agent Conversations**: See exactly what each agent says to each other
- **Decision Trees**: Watch how the supervisor chooses which agent to invoke
- **Tool Usage**: Track when agents search the web or read documents
- **Error Debugging**: Identify where things go wrong in complex workflows

**For Learning**: LangSmith transforms abstract multi-agent concepts into visual, understandable workflows. You'll see your agents working together in real-time.

**Setup**: Free tier includes 5,000 traces/month - more than enough for learning. Just sign up at [smith.langchain.com](https://smith.langchain.com/) and get your API key.

## Core Concepts Made Simple

### What is LangGraph?
LangGraph is like a flowchart for AI agents. Instead of one AI doing everything, you create a network where each AI has a specific job, and they pass information between each other.

**Think of it like a restaurant**:
- 🍽️ **Host** (Supervisor): Decides which table needs attention
- 👨‍🍳 **Chef** (Research Agent): Gathers ingredients (information)
- 🥗 **Prep Cook** (Writing Agent): Assembles the dish (content)
- 🍴 **Server** (Editor Agent): Presents the final product

### Multi-Agent Patterns

#### 1. **Supervisor Pattern**
One "manager" agent decides which "worker" agent should handle each task.

```python
# Simplified example
def supervisor_decides(task):
    if "research" in task:
        return "research_agent"
    elif "write" in task:
        return "writing_agent"
    else:
        return "editing_agent"
```

#### 2. **Shared Workspace**
Agents collaborate by reading and writing files in a shared directory (`content/data/`), like teammates working on a shared Google Drive.

## Hands-On Exercises

### Exercise 1: Modify an Agent (Phase 1)
**Time**: 15 minutes

1. Open `multiagent_refactored.ipynb`
2. Find the "DocWriter" agent creation
3. Change its personality from professional to casual
4. Run the notebook and observe the difference

**Expected Result**: Your writing agent should produce more informal content.

### Exercise 2: Add a New Tool (Phase 2)
**Time**: 30 minutes

1. Open `src/tools/search.py`
2. Create a new tool that searches for images
3. Add it to your research agent
4. Test with a query requiring visual information

**Expected Result**: Your agent can now find and reference images.

### Exercise 3: Create a New Agent Type (Phase 3)
**Time**: 45 minutes

1. Design a "Fact-Checker" agent
2. Add it to the authoring team in `src/graphs/authoring.py`
3. Give it tools to verify claims
4. Test with a controversial topic

**Expected Result**: Your system should validate factual claims before publishing.

## Project Structure (You'll Understand This After Phase 2)

```
📁 Multi-Agent LangGraph System
├── 📘 multiagent_refactored.ipynb     # 🌱 Start here - uses modular components
├── 🐍 demo_refactored.py              # Quick test script
├── 📁 src/                            # 🚀 Phase 3 - production architecture
│   ├── 🤖 agents/     # Agent creation (research, writing, editing)
│   ├── 📊 graphs/     # Workflow definitions (how agents connect)
│   ├── 🛠️ tools/      # Capabilities (search, documents, retrieval)
│   ├── 📋 states/     # Data structures (what information flows between agents)
│   └── ⚙️ utils/      # Configuration and helper functions
├── 📁 content/data/   # 🤝 Shared workspace (where agents collaborate)
└── 📁 data/          # Source documents for testing
```

## Common Issues & Solutions {#troubleshooting}

### Setup Problems

**❌ "uv command not found"**
```bash
# Install uv first
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**❌ "API key not working"**
- Verify your OpenAI key at [platform.openai.com](https://platform.openai.com/api-keys)
- Check Tavily key at [tavily.com](https://tavily.com/)
- Verify your LangSmith key at [smith.langchain.com](https://smith.langchain.com/)
- Ensure you've set environment variables in your current shell

**❌ "Module not found" errors**
```bash
# Make sure you're in the project directory
cd /path/to/Multi_Agent_with_LangGraph
uv sync
```

### Learning Problems

**❌ "The concepts are too complex"**
- Spend more time with Phase 1 - don't rush
- Focus on one notebook cell at a time
- Try explaining each concept to yourself in simple words

**❌ "My agents aren't working together"**
- Check the `content/data/` directory - do you see files being created?
- Look at the agent messages in the notebook output
- Start with simpler prompts and gradually increase complexity

**❌ "I can't see what my agents are doing"**
- Set up LangSmith for visual tracing (see setup section above)
- Without LangSmith, you're missing the most valuable learning tool
- Check your LangSmith project dashboard at [smith.langchain.com](https://smith.langchain.com/)

## Assessment: How Do You Know You're Ready?

### Phase 1 Complete When You Can:
- [ ] Explain what RAG means in your own words
- [ ] Describe how agents pass information between each other
- [ ] Run the basic notebook without errors

### Phase 2 Complete When You Can:
- [ ] Modify an agent's behavior by changing its prompt
- [ ] Add a new tool to an existing agent
- [ ] Explain why modular code is better than one big file

### Phase 3 Complete When You Can:
- [ ] Create a new agent and integrate it into a team
- [ ] Debug workflow issues using the shared workspace
- [ ] Design your own multi-agent workflow for a new problem

## Next Steps & Extensions

**Ready for More?** Try these projects:
1. **Personal Assistant System**: Create agents for email, calendar, and task management
2. **Content Creation Pipeline**: Build a system for blog posts, social media, and marketing materials
3. **Research Analysis Tool**: Develop agents for academic paper analysis and synthesis

## Key References

This implementation follows [LangGraph best practices](https://langchain-ai.github.io/langgraph/) including:
- [Multi-Agent Patterns](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) - How agents coordinate
- [State Management](https://langchain-ai.github.io/langgraph/concepts/low_level/) - How data flows between agents
- [Hierarchical Teams](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/) - Advanced coordination patterns

---

## 🌐 DeepWiki: Your Interactive Documentation Portal

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://app.devin.ai/wiki/donbr/langgraph_multiagent)

**DeepWiki provides an AI-powered interface to explore this project in depth.** Ask questions, get instant answers, and discover:

- 🏗️ **System Architecture**: Interactive diagrams showing how all components connect
- 📊 **Performance Analysis**: Detailed benchmarks comparing all 6 retrieval strategies
- 🔧 **Configuration Deep Dives**: Advanced settings and optimization techniques
- 💡 **Implementation Insights**: Code explanations and design decisions
- 🚀 **Scaling Strategies**: How to adapt this foundation for production use

Perfect for when you need quick answers or want to explore specific technical aspects without diving through all the code.

---

**🎯 Ready to Start?** Open `multiagent_refactored.ipynb` and begin your journey into multi-agent AI systems!
