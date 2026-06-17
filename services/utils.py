import json


def apply_filters(products, intent):
    """
    Apply deterministic filters extracted from intent.

    This function intentionally does NOT perform:
    - semantic matching
    - category inference
    - feature inference
    - ranking
    - recommendation logic

    Those should be handled by:
    - embeddings/vector search
    - LLM explanation layer
    """

    filtered = []

    brand = str(intent.get("brand", "")).strip().lower()
    category = str(intent.get("category", "")).strip().lower()

    min_price = intent.get("min_price", 0) or 0
    max_price = intent.get("max_price", 0) or 0

    required_features = [
        str(f).strip().lower()
        for f in intent.get("required_features", [])
        if f
    ]

    for product in products:

        # -----------------
        # Price filter
        # -----------------
        price = float(product.get("price", 0) or 0)

        if min_price and price < min_price:
            continue

        if max_price and price > max_price:
            continue

        # -----------------
        # Brand filter
        # -----------------
        if brand:
            product_name = str(
                product.get("product_name", "")
            ).lower()

            if brand not in product_name:
                continue

        # -----------------
        # Category filter
        # -----------------
        if category:
            product_category = str(
                product.get("category", "")
            ).lower()

            if category != product_category:
                continue

        # -----------------
        # Feature filter
        # -----------------
        if required_features:

            features_text = " ".join([
                str(product.get("features", "")),
                str(product.get("description", "")),
            ]).lower()

            if not all(
                    feature in features_text
                    for feature in required_features
            ):
                continue

        filtered.append(product)

    return filtered


def apply_sort(products, intent):
    """
    Generic sorting based on intent.

    Supported examples:
    - price_asc
    - price_desc
    - score_desc
    - score_asc
    - rating_desc
    - rating_asc
    """
    sort_preference = str(
        intent.get("sort_preference", "")
    ).strip().lower()

    if not sort_preference:
        return products

    try:
        field, order = sort_preference.rsplit("_", 1)
    except ValueError:
        return products

    reverse = order == "desc"

    return sorted(
        products,
        key=lambda p: p.get(field, 0) or 0,
        reverse=reverse
    )


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
