from langchain.agents import create_agent
from utils import Answer , llm
from tools.student_tools import student_tools
from tools.learning_tools import learning_tools
from tools.rag import sumarize_retrieved_documents
from tools.instructor_tools import extract_instructor_info
tools = [*student_tools , *learning_tools ,extract_instructor_info , sumarize_retrieved_documents]

system_prompt = open('system_prompt.txt' , 'r').read()

agent = create_agent(llm, tools = tools , system_prompt=system_prompt, response_format=Answer)
for i in range(3):
    user_input = input("Enter your question : ")
    answer =   agent.invoke({
        "messages": [{"role": "user", "content": user_input}]
    })
    print(answer["structured_response"].answer)
    print("\n------------------------------------------------------------\n")


