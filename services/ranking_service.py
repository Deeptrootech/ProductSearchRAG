class RankingService:

    def rank(self, products, intent):

        def score(p):

            base = p.get("score", 0)

            # feature match boost
            features = p.get("features", "").lower()

            for f in intent.get("required_features", []):
                if f.lower() in features:
                    base += 0.3

            # brand boost
            if intent.get("brand") and intent["brand"].lower() in p["product_name"].lower():
                base += 0.5

            # price preference (light)
            if intent.get("sort_preference") == "price_asc":
                base += 1 / (p.get("price", 1) + 1)

            return base

        return sorted(products, key=score, reverse=True)
