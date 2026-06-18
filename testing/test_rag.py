from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()
key = os.environ.get("GOOGLE_API_KEY")
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview" , 
    output_dimensionality = 500 ,
    task_type = "RETRIEVAL_DOCUMENT" , 
    api_key = key)
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
    collection_name="english_learning"
)
docs = vectorstore.similarity_search(query, k=3)

for doc in docs:
    print(doc.page_content)
#py testing\test_rag.py