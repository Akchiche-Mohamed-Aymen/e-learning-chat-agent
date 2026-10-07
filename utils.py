import os
from dotenv import load_dotenv
from pydantic import BaseModel
import json
import uuid
import os
from langchain_mistralai import ChatMistralAI , MistralAIEmbeddings
import os 
from dotenv import load_dotenv
load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
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
key = os.getenv("MISTRAL_API_KEY")
llm = ChatMistralAI(model="open-mistral-7b",api_key= key)
embeddings = MistralAIEmbeddings(model="mistral-embed",api_key= key)