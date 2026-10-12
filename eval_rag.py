import json
data = json.loads(open("./test/rag_test_dataset.json", "r", encoding="utf-8").read())
n = len(data)
def clean_doc(doc):
    doc = doc.split(": ")
    return doc[1].strip()

     
hit = 0
for i in range(n):
    docs = data[i]['docs']
    retrieved_docs = data[i]['retrieved_docs']
    retrieved_docs = [clean_doc(doc) for doc in retrieved_docs]
    data[i]['retrieved_docs'] = retrieved_docs
    for doc in retrieved_docs:
        if doc in docs:
            hit += 1
            break
mrr = 0
for i in range(n):
    docs = data[i]['docs']
    retrieved_docs = data[i]['retrieved_docs']
    rr = 0
    k = len(retrieved_docs)
    for j in range(k):
        if retrieved_docs[j]in docs:
            rr = 1/(j+1)
            break
    mrr += rr
print(f"Hit Rate: {hit}/{n} ({hit/n*100:.2f}%)")
print(f"MRR: {100*mrr/n:.2f}%")
with open("./test/rag_test_dataset.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
