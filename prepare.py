import json
data = json.loads(open("./test/rag_test_dataset.json", "r", encoding="utf-8").read())

    
prepared_data = {
    "user_input": [],
    "retrieved_contexts": [],
    "response": [],
    "reference": []
}
for item in data:
    prepared_data["user_input"].append(item['question'])
    prepared_data["retrieved_contexts"].append(item['retrieved_docs'])
    prepared_data["response"].append(item['llm_answer'])
    prepared_data["reference"].append(item['expected_answer'])
   
with open("./test/prepared_rag_test_dataset.json", "w", encoding="utf-8") as f:
    json.dump(prepared_data, f, ensure_ascii=False, indent=4)
