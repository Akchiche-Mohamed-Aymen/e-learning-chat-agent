from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage , SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.tools import tool
from pydantic import BaseModel
from utils import llm  , embeddings
#=======================================


vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
    collection_name="english_learning_platform"
)
class Answer(BaseModel):
    answer: str
#=============================================================
def get_documents_from_vector_db(query:str)->list:
    retrieved = []
    docs = vectorstore.similarity_search(query, k=3)
    for doc in docs:
        retrieved.append(doc.page_content)
    return retrieved
#@tool 
def sumarize_retrieved_documents(query :str)-> tuple[Answer , list]:
    """tool that retrieve answers from vetor db then summarize it """
    parser = JsonOutputParser(pydantic_object=Answer)
    prompt_template = PromptTemplate(
    template="{user_prompt}\n\n{format_instructions}",
    input_variables=["user_prompt"],
     partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    formatted_prompt = prompt_template.format(user_prompt= query)
    docs =  get_documents_from_vector_db(query)
    if not docs:
        return Answer(answer="No relevant documents found in the knowledge base."), []
    knowldge = "\n".join(docs)
    system_prompt = f"""
    you are a hepful assistant that takes the docs found in the knowldge  , and query of the user , summarize the docs retrieved
    and give answer based on the given docs in the knowledge base for the query as human , answer should be meduim , understandable
    **knowldge** =  {knowldge}
    -Rules:
        * Output must have schema of the responseClass : {Answer.model_json_schema()}
""" 
    messages = [SystemMessage(content = system_prompt ), HumanMessage(content=formatted_prompt)]
    response = llm.invoke(messages)
    return parser.parse(response.content) , docs


