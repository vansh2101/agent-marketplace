import spacy
import chromadb
import numpy as np
import ollama
import chromadb

client = chromadb.Client()

nlp = spacy.load('en_core_web_lg')
def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def create_vector_db_from_text(file_path):
    text = read_text_from_file(file_path)
    serialized_convo = f"document_text: {text}"
    
    vector_db_name = "text_conversations"

    try:
        client.delete_collection(name=vector_db_name)
    except ValueError:
        pass

    vector_db = client.create_collection(name=vector_db_name)

    doc = nlp(serialized_convo)
    embedding = doc.vector

    vector_db.add(
        ids=['1'], 
        embeddings=[embedding.tolist()],  
        documents=[serialized_convo]
    )
def stream_response(prompt):
    convo.append({'role': 'user', 'content': prompt})
    response = ''
    stream = ollama.chat(model='tinyllama:latest ', messages=convo, stream=True)
    print('\nASSISTANT:\n')
    for chunk in stream:
        content = chunk['message']['content']
        response += content
        print(content, end='', flush=True)
    print('\n')
    convo.append({'role': 'assistant', 'content': response})

def retrieve_embeddings(prompt):
    doc = nlp(prompt)
    prompt_embedding = doc.vector

    vector_db = client.get_collection(name='text_conversations')
    results = vector_db.query(query_embeddings=[prompt_embedding.tolist()], n_results=1)
    best_embedding = results['documents'][0][0]

    return best_embedding

file_path = r"C:\Users\Yatharth\Desktop\desktop1\AI\isro_hack\hypothetical_flood_Data.txt"  
create_vector_db_from_text(file_path)

convo = []

while True:
    user_prompt = input('USER:\n')
    context = retrieve_embeddings(prompt=user_prompt)
    enhanced_prompt = f'USER PROMPT: {user_prompt} \nCONTEXT FROM EMBEDDINGS: {context}'
    stream_response(enhanced_prompt)
