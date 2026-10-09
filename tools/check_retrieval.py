import json
data = json.loads(open("./test/rag_test_dataset.json", "r", encoding="utf-8").read())
def compare(docs , retrieved_docs):
    s = 0
    for doc in retrieved_docs:
        if doc.replace(" :", ":") in docs:
            s += 1
    return s
s = 0
for item in data:
    docs = item['docs']
    retrieved_docs = item['retrieved_docs']
    s += compare(docs, retrieved_docs)
print(round(s / 300, 2))
#0.6