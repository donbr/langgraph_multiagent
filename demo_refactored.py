#!/usr/bin/env python3
"""
Simplified demo of the refactored multi-agent LangGraph system.
This demonstrates the modular architecture without the full complexity.
"""

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from src import (
    setup_environment,
    get_llm,
    create_rag_graph,
    create_research_graph,
    create_authoring_graph,
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


def main():
    """Run the refactored multi-agent system demo."""
    print("🚀 Starting Multi-Agent LangGraph System Demo")
    print("=" * 50)
    
    # 1. Setup and Configuration
    print("\n1. Setting up environment...")
    setup_environment()
    print("✅ Environment configured")
    
    # 2. Load and Process Documents
    print("\n2. Loading and processing documents...")
    loan_knowledge_resources = load_loan_documents()
    print(f"✅ Loaded {len(loan_knowledge_resources)} loan documents")
    
    # Use subset for faster demo
    text_splitter = create_text_splitter(chunk_size=750, chunk_overlap=0)
    loan_knowledge_chunks = text_splitter.split_documents(loan_knowledge_resources[:50])
    print(f"✅ Created {len(loan_knowledge_chunks)} chunks (using subset for demo)")
    
    complaints = load_complaints()
    print(f"✅ Loaded {len(complaints)} complaints")
    
    # 3. Create Vector Stores
    print("\n3. Creating vector stores...")
    qdrant_vectorstore = create_vectorstore(loan_knowledge_chunks)
    qdrant_retriever = qdrant_vectorstore.as_retriever()
    
    qdrant_complaint_vectorstore = create_vectorstore(complaints[:100])  # Subset for demo
    qdrant_complaint_retriever = qdrant_complaint_vectorstore.as_retriever()
    print("✅ Vector stores created")
    
    # 4. Initialize Language Models
    print("\n4. Initializing language models...")
    llm = get_llm("gpt-4o-mini")
    nano_llm = get_nano_llm()
    print("✅ Language models ready")
    
    # 5. Create and Test RAG Graph
    print("\n5. Testing RAG functionality...")
    rag_graph = create_rag_graph(qdrant_retriever, nano_llm)
    
    rag_result = rag_graph.invoke({"question": "What is the maximum loan amount?"})
    print("✅ RAG Response:")
    print(f"   {rag_result['response']}")
    
    # 6. Test Research Team
    print("\n6. Testing research team...")
    research_graph = create_research_graph(llm, rag_graph)
    print("✅ Research graph created")
    
    # Test research with a simple question
    from src.graphs.supervisor import create_chains
    research_chain, _ = create_chains(research_graph, None)
    
    print("\n📊 Research Team Results:")
    count = 0
    for s in research_chain.stream("What are Pell Grants?", {"recursion_limit": 10}):
        if "__end__" not in s:
            if 'messages' in s:
                for node_name, data in s.items():
                    if 'messages' in data and data['messages']:
                        print(f"   {node_name}: {data['messages'][0].content[:150]}...")
            count += 1
            if count > 2:  # Limit output
                break
    
    # 7. Test Document Creation
    print("\n7. Testing document creation...")
    working_directory = create_working_directory()
    print(f"✅ Working directory: {working_directory}")
    
    authoring_graph = create_authoring_graph(llm, working_directory, qdrant_complaint_retriever)
    print("✅ Authoring graph created")
    
    # 8. Architecture Summary
    print("\n8. Architecture Overview:")
    print("✅ Modular Structure:")
    print("   📁 src/agents/     - Agent creation functions")
    print("   📁 src/tools/      - Tool implementations")
    print("   📁 src/graphs/     - Graph construction")
    print("   📁 src/states/     - Type-safe state definitions")
    print("   📁 src/utils/      - Configuration & utilities")
    
    print("\n✅ Benefits of Refactored Architecture:")
    print("   🔧 Modularity: Single responsibility per module")
    print("   🔒 Type Safety: Comprehensive TypedDict usage")
    print("   ♻️  Reusability: Easy to import and compose")
    print("   🧪 Testability: Individual components can be tested")
    print("   📈 Scalability: Easy to extend with new agents/tools")
    
    print("\n🎉 Demo completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()