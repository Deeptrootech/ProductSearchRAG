import json


def apply_filters(products, intent):
    filters = intent.get("filters", [])

    filtered = []
    for product in products:
        keep = True
        for rule in filters:
            field = rule.get("field")
            operator = rule.get("operator")
            value = rule.get("value")

            product_value = product.get(field)

            if product_value is None:
                break

            try:

                if operator == "eq":
                    keep = product_value == value

                elif operator == "neq":
                    keep = product_value != value

                elif operator == "gt":
                    keep = product_value > value

                elif operator == "gte":
                    keep = product_value >= value

                elif operator == "lt":
                    keep = product_value < value

                elif operator == "lte":
                    keep = product_value <= value

                elif operator == "contains":
                    keep = str(value).lower() in str(product_value).lower()

                else:
                    keep = True
            except Exception:
                keep = False
            if not keep:
                break
        if keep:
            filtered.append(product)
    return filtered


def apply_sort(products, intent):

    sort_config = intent.get("sort", {})

    field = sort_config.get("field")
    order = sort_config.get("order", "asc")

    if not field:
        return products

    reverse = order == "desc"

    return sorted(
        products,
        key=lambda p: p.get(field, 0),
        reverse=reverse
    )


def format_context(products):
    cleaned = []

    for p in products:
        cleaned.append({
            "product_name": p.get("product_name"),
            "price": p.get("price"),
            "rating": p.get("rating"),
            "stock": p.get("stock"),
            "brand": p.get("brand"),
            "category": p.get("category"),
            "features": p.get("features"),
            "description": p.get("description"),
        })

    return json.dumps(cleaned, indent=2)
