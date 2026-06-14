import json


def build_intent_filter(intent):
    filters = []

    if intent.get("min_price", 0) > 0:
        filters.append(f"price >= {intent['min_price']}")

    if intent.get("max_price", 0) > 0:
        filters.append(f"price <= {intent['max_price']}")

    if intent.get("category"):
        filters.append(
            f'category == "{intent["category"]}"'
        )

    return " and ".join(filters)


def format_product_context(products):
    cleaned_products = []

    for p in products:
        cleaned_products.append({
            "product_name": p.get("product_name"),
            "category": p.get("category"),
            "price": p.get("price"),
            "features": p.get("features"),
            "description": p.get("description"),
            "score": p.get("score")
        })

    return json.dumps(
        cleaned_products,
        indent=2,
        ensure_ascii=False
    )
