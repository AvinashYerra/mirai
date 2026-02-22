import random
import uuid
from datetime import datetime
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

PRODUCTS = [
    {"type": "vaccine", "temp_range": (2, 8)},
    {"type": "food", "temp_range": (4, 10)},
    {"type": "electronics", "temp_range": (15, 35)},
]

ROUTES = ["BLR-MUM", "DEL-KOL", "HYD-CHN", "PUN-DEL"]
CHECKPOINTS = ["MANUFACTURER", "WAREHOUSE", "RETAILER", "OUT_FOR_DELIVERY"]


def build_event_text(event):
    return (
        f"{event['product_type']} shipment on route {event['route']} "
        f"at checkpoint {event['checkpoint']} "
        f"with temperature {event['temperature']}°C, "
        f"expected quantity {event['quantity_expected']} "
        f"but received {event['quantity_received']}."
    )


def enrich_risk(event):
    flags = []
    score = 0

    if event["quantity_received"] < event["quantity_expected"]:
        flags.append("QUANTITY_MISMATCH")
        score += 1

    if event["product_type"] == "vaccine" and not (2 <= event["temperature"] <= 8):
        flags.append("TEMP_VIOLATION")
        score += 2

    if event["product_type"] == "food" and not (4 <= event["temperature"] <= 10):
        flags.append("TEMP_VIOLATION")
        score += 1

    event["risk_flags"] = flags
    event["risk_score"] = score
    return event


def generate_shipment_event():
    product = random.choice(PRODUCTS)
    temp_min, temp_max = product["temp_range"]

    event = {
        "shipment_id": str(uuid.uuid4()),
        "product_type": product["type"],
        "route": random.choice(ROUTES),
        "checkpoint": random.choice(CHECKPOINTS),
        "temperature": round(random.uniform(temp_min - 3, temp_max + 5), 2),
        "quantity_expected": 100,
        "quantity_received": random.choice([100, 100, 98, 95]),
        "timestamp": datetime.utcnow().isoformat()
    }

    event["event_text"] = build_event_text(event)
    event = enrich_risk(event)

    event["embedding"] = model.encode(event["event_text"]).tolist()
    return event


if __name__ == "__main__":
    print(generate_shipment_event())