import json
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview" , output_dimensionality = 500 , task_type = "RETRIEVAL_DOCUMENT")
knowledge  = json.load(open('./data/knowledge.json','r',encoding='utf-8'))
content = [f'{item["title"]} : {item["content"]}' for item in knowledge]
vectorstore = Chroma.from_texts(
    texts=content,
    id= [str(i) for i in range(len(content))],
    metadatas=knowledge,
    embedding=embeddings,
    persist_directory="./chroma_db",
    collection_name="english_learning_platform"
)
#py embed_knowledge.py