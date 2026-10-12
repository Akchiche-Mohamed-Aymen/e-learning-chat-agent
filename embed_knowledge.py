import json
from langchain_chroma import Chroma
from utils import embeddings
knowledge  = json.load(open('./data/knowledge.json','r',encoding='utf-8'))
content = [item["content"] for item in knowledge]
ids = [item["title"] for item in knowledge]
try:
    vectorstore = Chroma.from_texts(
        texts=content,
        ids= ids,
        metadatas=ids,
        embedding=embeddings,
        persist_directory="./chroma_db",
        collection_name="english_learning_platform"
    )

except Exception as e:
    print(f" {e}")
#py embed_knowledge.py