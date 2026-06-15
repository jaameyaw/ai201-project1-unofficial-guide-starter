import sys
sys.path.insert(0, 'src')
from unofficial_guide.pipeline import ask
from pathlib import Path

question = 'What do students say to do if on-campus housing is full and they are on a waitlist?'
print('Testing retrieval with:', question)
result = ask(question, Path('chroma_db'), top_k=4)
print('\nAnswer (first 500 chars):', result['answer'][:500])
print('\nSources:', result['sources'])
print(f'Retrieved {len(result["retrieved_chunks"])} chunks')
