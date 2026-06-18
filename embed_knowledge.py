import json
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import os 
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("GOOGLE_API_KEY")
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview" , 
    output_dimensionality = 500 ,
    task_type = "RETRIEVAL_DOCUMENT" , 
    api_key = key)
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