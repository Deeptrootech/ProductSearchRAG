def format_product_context(products):
    if not products:
        return "No products found."

    context = ""
    for idx, product in enumerate(products, start=1):
        context += f"""
                    Product {idx}
                    Name: {product.get('product_name')}
                    Category: {product.get('category')}
                    Price: ${product.get('price')}
                    Features: {product.get('features')}
                    Description: {product.get('description')}
                    Similarity Score: {product.get('score')}
                    """
    return context
