import json
from ragas.metrics import answer_relevancy, faithfulness, context_precision, context_recall
from ragas import evaluate
from utils import llm , embeddings
from datasets import Dataset
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

evaluator_llm = LangchainLLMWrapper(llm)
evaluator_embeddings = LangchainEmbeddingsWrapper(embeddings)
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
   
dataset = Dataset.from_dict(prepared_data)

results = evaluate(
    dataset=dataset,
    metrics=[answer_relevancy, faithfulness,
             context_precision, context_recall],
    llm=evaluator_llm,
    embeddings=evaluator_embeddings
)
print("\n=== RAGAS Evaluation Results ===")
print(results)