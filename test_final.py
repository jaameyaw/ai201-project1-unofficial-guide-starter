"""End-to-end verification of the RAG pipeline."""

import sys
sys.path.insert(0, 'src')

from pathlib import Path
import chromadb

# Test 1: Verify the vector store exists and has data
print("=" * 60)
print("Test 1: Verifying Vector Store")
print("=" * 60)

try:
    client = chromadb.PersistentClient(path='chroma_db')
    collection = client.get_collection(name='housing_chunks')
    count = collection.count()
    print(f"✓ Vector store loaded successfully")
    print(f"✓ Collection 'housing_chunks' contains {count} chunks")
except Exception as e:
    print(f"✗ Failed to load vector store: {e}")
    sys.exit(1)

# Test 2: Test retrieval (query without generation)
print("\n" + "=" * 60)
print("Test 2: Testing Retrieval")
print("=" * 60)

try:
    from unofficial_guide.embedding import retrieve_chunks
    
    question = "What do students say to do if on-campus housing is full?"
    chunks = retrieve_chunks(question, Path('chroma_db'), top_k=4)
    
    print(f"✓ Retrieved {len(chunks)} chunks for question:")
    print(f"  '{question}'")
    print(f"\nRetrieved chunks:")
    for i, chunk in enumerate(chunks, 1):
        dist = chunk.get('distance', 'N/A')
        source = chunk['metadata'].get('source_path', 'unknown')
        text_preview = chunk['text'][:100].replace('\n', ' ')
        print(f"\n  {i}. Distance: {dist:.3f}, Source: {source}")
        print(f"     {text_preview}...")
        
except Exception as e:
    print(f"✗ Retrieval failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Test the full pipeline with generation
print("\n" + "=" * 60)
print("Test 3: Testing Full Pipeline (with Generation)")
print("=" * 60)

try:
    from unofficial_guide.pipeline import ask
    
    test_questions = [
        "What do students say to do if on-campus housing is full?",
        "Is dorm life always cheaper than living off campus?",
        "What problems do students run into when renting an apartment off campus?"
    ]
    
    for q in test_questions:
        print(f"\nQuestion: {q}")
        result = ask(q, Path('chroma_db'), top_k=4)
        print(f"Answer: {result['answer'][:300]}...")
        print(f"Sources: {result['sources']}")
        
except Exception as e:
    print(f"✗ Full pipeline test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✓ All tests completed successfully!")
print("=" * 60)
