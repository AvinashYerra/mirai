from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

es = Elasticsearch(
    cloud_id="YOUR_CLOUD_ID",
    api_key="YOUR_API_KEY"
)

INDEX_NAME = "shipment_risks"


def analyze_intent_llm(user_query):
    """
    Mocked LLM output for blog clarity.
    In real version, this comes from GPT/Gemini.
    """
    intent = {
        "search_text": user_query,
        "risk_flags": []
    }

    if "temperature" in user_query or "spoilage" in user_query:
        intent["risk_flags"].append("TEMP_VIOLATION")

    if "quantity" in user_query or "missing" in user_query:
        intent["risk_flags"].append("QUANTITY_MISMATCH")

    return intent


def build_elastic_query(search_text, risk_flags):
    query_vector = model.encode(search_text).tolist()

    query = {
        "size": 5,
        "query": {
            "bool": {
                "must": [
                    {
                        "knn": {
                            "field": "embedding",
                            "query_vector": query_vector,
                            "k": 5,
                            "num_candidates": 100
                        }
                    }
                ],
                "filter": []
            }
        }
    }

    if risk_flags:
        query["query"]["bool"]["filter"].append({
            "terms": {"risk_flags": risk_flags}
        })

    return query


def explain_results_llm(results):
    explanations = []

    for hit in results["hits"]["hits"]:
        src = hit["_source"]
        explanations.append(
            f"- Shipment `{src['shipment_id']}` is risky due to "
            f"{', '.join(src['risk_flags']) or 'contextual anomalies'} "
            f"on route {src['route']} at {src['checkpoint']}."
        )

    return "\n".join(explanations)


def risk_agent(user_query):
    intent = analyze_intent_llm(user_query)
    es_query = build_elastic_query(
        intent["search_text"],
        intent["risk_flags"]
    )

    results = es.search(index=INDEX_NAME, body=es_query)
    return explain_results_llm(results)


if __name__ == "__main__":
    query = "shipments with temperature issues or spoilage risk"
    print(risk_agent(query))