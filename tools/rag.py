from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from langchain_core.messages import HumanMessage , SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from langchain.tools import tool
from pydantic import BaseModel
from utils import llm
load_dotenv()
#=======================================
embed_key = os.environ.get("EMBEDDING")
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview" , 
    output_dimensionality = 500 ,
    task_type = "RETRIEVAL_DOCUMENT" , 
    api_key = embed_key)

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
    collection_name="english_learning_platform"
)
class Answer(BaseModel):
    answer: str
#=============================================================
def get_documents_from_vector_db(query:str)->str:
    retrieved = ''
    docs = vectorstore.similarity_search(query, k=3)
    for doc in docs:
        retrieved+=doc.page_content
    return retrieved
#@tool 
def sumarize_retrieved_documents(query):
    """tool that retrieve answers from vetor db then summarize it """
    parser = JsonOutputParser(pydantic_object=Answer)
    prompt_template = PromptTemplate(
    template="{user_prompt}\n\n{format_instructions}",
    input_variables=["user_prompt"],
     partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    formatted_prompt = prompt_template.format(user_prompt= query)
    knowldge =  get_documents_from_vector_db(query)
    system_prompt = f"""
 you are a hepful assistant that takes the docs found in the knowldge  , and query of the user , summarize the docs retrieved
 and give answer for the query as human , answer should be meduim , understandable
    **knowldge** =  {knowldge}
    -Rules:
        * Output must have schema of the responseClass : {Answer.model_json_schema()}
""" 
    messages = [SystemMessage(content = system_prompt ), HumanMessage(content=formatted_prompt)]
    response = llm.invoke(messages)
    return parser.parse(response.content)


