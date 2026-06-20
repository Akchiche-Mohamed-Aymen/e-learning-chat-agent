from langchain_google_genai import GoogleGenerativeAIEmbeddings 
import os , json
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
embed_key = os.environ.get("EMBEDDING")
embed_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview" , 
    output_dimensionality = 500 ,
    task_type = "RETRIEVAL_DOCUMENT" , 
    api_key = embed_key)
answers  = json.load(open("testing/answers.json",'r',encoding='utf-8'))
evaluation = []
n = len(answers)
for i in range(n):
    vec1 = [embed_model.embed_query(text = answers[i]['rag'])]
    vec2 = [embed_model.embed_query(text = answers[i]['expected'])]
    cosine = cosine_similarity(vec1 , vec2)[0][0]
    evaluation.append(cosine)
print(evaluation)
#py testing\evaluate_rag.py
