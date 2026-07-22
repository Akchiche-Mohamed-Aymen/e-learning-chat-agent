from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from utils import Answer , llm , load_id
from tools.student_tools import student_tools
from tools.learning_tools import learning_tools
from tools.rag import sumarize_retrieved_documents
from tools.instructor_tools import extract_instructor_info
from history_data.history import save_history , get_summary_history , retrieve_history_db 
tools = [*student_tools , *learning_tools ,extract_instructor_info , sumarize_retrieved_documents]
history_system_prompt = open('history_system.txt' , 'r').read()
history_agent = create_agent(llm, tools = [get_summary_history , retrieve_history_db ] , system_prompt=history_system_prompt)

system_prompt = open('system_prompt.txt' , 'r').read()
user_id = load_id()
config = {
    "configurable": {
        "thread_id": user_id
    }
}
memory = InMemorySaver()
agent = create_agent(llm, tools = tools , system_prompt=system_prompt, response_format=Answer , checkpointer=memory , name='Aymen_English')
for _ in range(5):
    user_input = input("Enter your question : ")
    try:
        #history_context = history_agent.invoke({ "messages": [{"role": "user","content": user_input}]})["messages"][-1].content
        answer =   agent.invoke({
                "messages": [
                    
                {
                    "role": "user",
                    "content": user_input
                }]
            } , config=config)
        res = answer["structured_response"].answer
        save = answer["structured_response"].add_to_db
        print(res)
        print(save)
        save_history(user_id , user_input , res ,save)
    
    except Exception as ex:
        print(ex)
        break