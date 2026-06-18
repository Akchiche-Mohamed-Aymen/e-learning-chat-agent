from langchain_google_genai import ChatGoogleGenerativeAI
from tools import tools_list
from langchain.agents import create_agent
from pydantic import BaseModel

class Answer(BaseModel):
    answer: str
    tools_used: list[str]
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=1.0, 
    max_retries=2)
system_prompt = """You are a helpful assistant that can answer questions about the weather and student grades.
You have access to the following tools:
1. fetch_weather(city, convert_to_celsius): returns the current weather in a given city (if city not found use Ouargla as default).
2. getGrade(student_name): returns the grade of a student given their name.
When a user asks a question, you should determine which tool to use and provide the appropriate response. If the user asks about the weather, use the fetch_weather tool. If the user asks about student grades, use the getGrade tool. Always provide a clear and concise answer to the user's question.
final answer should be as human format , not just the combination of outputs from used tools
"""
try:
    agent = create_agent(llm, tools = tools_list , system_prompt=system_prompt, response_format=Answer)
    
except Exception as e:
    print(f"An error occurred: {e}")