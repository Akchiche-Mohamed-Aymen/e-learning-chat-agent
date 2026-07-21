import json
from langchain_chroma import Chroma
from utils import embeddings
knowledge  = json.load(open('./data/knowledge.json','r',encoding='utf-8'))
content = [f'{item["title"]} : {item["content"]}' for item in knowledge]
try:
    vectorstore = Chroma.from_texts(
        texts=content,
        ids= [str(i) for i in range(len(content))],
        metadatas=knowledge,
        embedding=embeddings,
        persist_directory="./chroma_db",
        collection_name="english_learning_platform"
    )

except Exception as e:
    print(f" {e}")
#py embed_knowledge.py