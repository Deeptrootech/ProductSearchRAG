import json


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
