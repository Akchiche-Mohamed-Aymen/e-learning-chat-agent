import json
from langchain_chroma import Chroma
from utils import embeddings
knowledge  = json.load(open('./data/knowledge.json','r',encoding='utf-8'))
content = [item["content"] for item in knowledge]
ids = [{"topic": item["title"]} for item in knowledge]
try:
    vectorstore = Chroma.from_texts(
        texts=content,
        ids= [f'Topic {i+1}' for i in range(len(content))],
        metadatas=ids,
        embedding=embeddings,
        persist_directory="./chroma_db",
        collection_name="english_learning_platform"
    )
    print("Knowledge embedding completed successfully.")
except Exception as e:
    print(f" {e}")
#py embed_knowledge.py