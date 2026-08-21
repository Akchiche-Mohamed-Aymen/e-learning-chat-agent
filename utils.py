from langchain_google_genai import   ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import json
import uuid
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os 
from dotenv import load_dotenv

USER_FILE = "user.json"
def load_id():
   
        try:
            with open(USER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "id" in data:
                return data["id"]
        except (json.JSONDecodeError, OSError):
            user_id = str(uuid.uuid4())
            with open(USER_FILE, "w", encoding="utf-8") as f:
                json.dump({"id": user_id}, f, indent=4)

            return user_id
class Answer(BaseModel):
    answer: str
    add_to_db : bool
    tools_used: list[str]
load_dotenv()
key = os.environ.get("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash" , api_key =key , temperature=0.2 ,  max_retries=2)


embed_key = os.environ.get("EMBEDDING")
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview" , 
    output_dimensionality = 500 ,
    task_type = "RETRIEVAL_DOCUMENT" , 
    api_key = embed_key)
