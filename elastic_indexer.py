from elasticsearch import Elasticsearch
from data_generator import generate_shipment_event

INDEX_NAME = "shipment_risks"

es = Elasticsearch(
    cloud_id="YOUR_CLOUD_ID",
    api_key="YOUR_API_KEY"
)


def create_index():
    if es.indices.exists(index=INDEX_NAME):
        return

    mapping = {
        "mappings": {
            "properties": {
                "shipment_id": {"type": "keyword"},
                "product_type": {"type": "keyword"},
                "route": {"type": "keyword"},
                "checkpoint": {"type": "keyword"},
                "risk_flags": {"type": "keyword"},
                "risk_score": {"type": "integer"},
                "event_text": {"type": "text"},
                "embedding": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine"
                },
                "timestamp": {"type": "date"}
            }
        }
    }

    es.indices.create(index=INDEX_NAME, body=mapping)


def index_events(n=20):
    for _ in range(n):
        event = generate_shipment_event()
        es.index(index=INDEX_NAME, document=event)


if __name__ == "__main__":
    create_index()
    index_events()
    print("Indexed shipment events into Elastic")