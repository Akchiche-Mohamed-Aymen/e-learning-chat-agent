import json
data = json.loads(open("./test/rag_test_dataset.json", "r", encoding="utf-8").read())
hit = 0
n = len(data)
for i in range(n):
    docs = data[i]['docs']
    retrieved_docs = data[i]['retrieved_docs']
    for doc in retrieved_docs:
        if doc.replace(" :" , ":") in docs:
            hit += 1
            break
mrr = 0
for i in range(n):
    docs = data[i]['docs']
    retrieved_docs = data[i]['retrieved_docs']
    rr = 0
    k = len(retrieved_docs)
    for j in range(k):
        if retrieved_docs[j].replace(" :" , ":") in docs:
            rr = 1/(j+1)
            break
    mrr += rr
print(f"Hit Rate: {hit}/{n} ({hit/n*100:.2f}%)")
print(f"MRR: {100*mrr/n:.2f}%")
