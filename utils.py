from langchain_google_genai import   ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()
key = os.environ.get("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash" , api_key =key , temperature=0.2 ,  max_retries=2)
