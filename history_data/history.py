from json import load , dump
from langchain_chroma import Chroma
from langchain_core.documents import Document
from utils import embeddings
from langchain.tools import tool
try:
    chat_histories = load(open('./history_data/chats.json'))
except:
    chat_histories = {}
history_db = Chroma(
    collection_name="history",
    persist_directory="./chroma_history",
    embedding_function=embeddings
)

def save_history_db(user_id: str, user_question: str, ai_answer: str):
    doc = Document(
        page_content=f"User: {user_question}\nAssistant: {ai_answer}",
        metadata={"user_id": user_id},
        id=user_id
    )
    history_db.add_documents([doc])
def get_history(user_id):
    return chat_histories.get(user_id , [])
def save_history(user_id , human , ai , save = False):
    if not save:
        return 
    history = get_history(user_id)
    history.append({
        'Human' : human,
        'AI' : ai
    })
    chat_histories[user_id] = history
    with open('./history_data/chats.json', "w", encoding="utf-8") as file:
        dump(chat_histories, file, indent=4, ensure_ascii=False)
    save_history_db(user_id , human , ai)

@tool
def retrieve_history_db(user_id: str, query: str, k: int = 3):
    """
    Retrieve relevant conversation history for a user.
    Use this tool when the query is somewhat clear
    Use this tool when previous conversations may help answer the current
    question. It returns only conversations whose relevance score is above
    the specified threshold. If no relevant history exists, it returns None.
    """

    results = history_db.similarity_search_with_relevance_scores(
        query=query,
        k=k,
        filter={"user_id": user_id}
    )
    threshold = 0.65
    history = [
        doc.page_content
        for doc, score in results
        if score >= threshold
    ]

    return '\n'.join(history) if history else ''
@tool
def get_summary_history(user_id):
    """
    Returns a concise summary of the user's past conversations.

    Use this tool when:
    - no relevant previous conversations can be retrieved,
    - a high-level understanding of the user's previous interactions is sufficient.

    Do NOT use this tool if relevant conversation history is available.
    In that case, use retrieve_history_db instead.
    The returned summary is intended to provide context for another AI assistant,
    not to directly answer the user's question.
    """
    history = get_history(user_id)
    if not history:
        return ''
    text = ''
    n = len(history)
    for i in range(n):
        text +=f'Human : {history[i]['Human']} , AI : {history[i]['AI']}'
    return text