from json import load , dump
try:
    chat_histories = load(open('./history_data/chats.json'))
except:
    chat_histories = {}

def get_history(user_id):
    return chat_histories.get(user_id , [])
def save_history(user_id , human , ai):
    history = get_history(user_id)
    history.append({
        'Human' : human,
        'AI' : ai
    })
    chat_histories[user_id] = history
    with open('./history_data/chats.json', "w", encoding="utf-8") as file:
        dump(chat_histories, file, indent=4, ensure_ascii=False)