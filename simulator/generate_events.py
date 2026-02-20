import random
import uuid
import time
from datetime import datetime

PRODUCTS = [
    {"type": "vaccine", "temp_range": (2, 8)},
    {"type": "food", "temp_range": (4, 10)},
    {"type": "electronics", "temp_range": (15, 35)},
]

ROUTES = [
    "BLR-MUM",
    "DEL-KOL",
    "HYD-CHN",
    "PUN-DEL"
]

CHECKPOINTS = [
    "MANUFACTURER",
    "WAREHOUSE",
    "RETAILER",
    "OUT_FOR_DELIVERY"
]


def generate_shipment_event():
    product = random.choice(PRODUCTS)

    temp_min, temp_max = product["temp_range"]
    temperature = round(random.uniform(temp_min - 3, temp_max + 5), 2)

    expected_qty = 100
    received_qty = random.choice([100, 100, 98, 95])

    event = {
        "shipment_id": str(uuid.uuid4()),
        "product_type": product["type"],
        "route": random.choice(ROUTES),
        "checkpoint": random.choice(CHECKPOINTS),
        "temperature": temperature,
        "quantity_expected": expected_qty,
        "quantity_received": received_qty,
        "timestamp": datetime.utcnow().isoformat()
    }

    return event


if __name__ == "__main__":
    print("Starting shipment event simulator...\n")
    while True:
        event = generate_shipment_event()
        print(event)
        time.sleep(3)