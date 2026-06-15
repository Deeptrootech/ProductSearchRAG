import json


def apply_filters(products, intent):
    filtered = []

    for p in products:

        price = p.get("price", 0)

        if intent.get("max_price") and price > intent["max_price"]:
            continue

        if intent.get("min_price") and price < intent["min_price"]:
            continue

        if intent.get("brand"):
            if intent["brand"].lower() not in p["product_name"].lower():
                continue

        filtered.append(p)

    return filtered


def format_context(products):
    cleaned = []

    for p in products:
        cleaned.append({
            "product_name": p.get("product_name"),
            "price": p.get("price"),
            "category": p.get("category"),
            "features": p.get("features"),
            "description": p.get("description"),
        })

    return json.dumps(cleaned, indent=2)
