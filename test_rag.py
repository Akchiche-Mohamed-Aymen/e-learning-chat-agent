from tools.rag import sumarize_retrieved_documents
import json
from time import sleep
data = json.loads(open("./test/rag_test_dataset.json", "r", encoding="utf-8").read())

try:
    with open("index.json", "r", encoding="utf-8") as f:
        i = json.load(f)["index"]
except :
    i = 0
while i < 100:
    try:
        rag_ans = sumarize_retrieved_documents(data[i]['question'])
        retrieved_docs = rag_ans[1]
        answer = rag_ans[0]['answer']
        data[i]['retrieved_docs'] = retrieved_docs
        data[i]['llm_answer'] = answer
        print(f"Finish Question {i+1} / 100")
        i += 1
        sleep(3)
    except Exception as e:
        print(f"Error processing index {i}: {e}")
        with open("index.json", "w", encoding="utf-8") as f:
            json.dump({"index": i}, f)
        break
with open("./test/rag_test_dataset.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)