import json
import sys
from pathlib import Path

sys.path.insert(0, 'src')

from unofficial_guide.pipeline import ask

QUESTIONS = [
    {
        'question': 'What do students say to do if on-campus housing is full?',
        'expected': 'Look for off-campus housing, ask about emergency housing or temporary placements, and use leftover financial aid or loans for rent if allowed.',
    },
    {
        'question': 'Is dorm life always cheaper than living off campus?',
        'expected': 'No. Students say it depends on the school; off-campus can be cheaper, but utilities, transportation, and furnishings can change the total cost.',
    },
    {
        'question': 'What problems do students run into when trying to rent an apartment off campus?',
        'expected': 'Lack of credit history, rental history, and income can make approval difficult.',
    },
    {
        'question': 'What makes freshmen consider living off campus anyway?',
        'expected': 'Lower cost, more comfort, roommate matching, and the ability to choose a better housing setup.',
    },
    {
        'question': 'What advice do students give about choosing a dorm room or floor?',
        'expected': 'Pick based on noise, privacy, and convenience rather than assuming there is one universally best floor.',
    },
]

results = []
for item in QUESTIONS:
    print('=' * 80)
    print('Question:', item['question'])
    print('-' * 80)
    result = ask(item['question'], Path('chroma_db'), top_k=4)
    print('Expected:', item['expected'])
    print('Answer:', result['answer'])
    print('Sources:', result['sources'])
    print()

    results.append(
        {
            'question': item['question'],
            'expected': item['expected'],
            'answer': result['answer'],
            'sources': result['sources'],
            'retrieved_chunks': [
                {
                    'distance': chunk.get('distance'),
                    'source_path': chunk.get('metadata', {}).get('source_path'),
                    'document_title': chunk.get('metadata', {}).get('document_title'),
                    'chunk_index': chunk.get('metadata', {}).get('chunk_index'),
                    'text': chunk.get('text'),
                }
                for chunk in result['retrieved_chunks']
            ],
        }
    )

Path('evaluation_results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
print('=' * 80)
print('Wrote evaluation_results.json')
