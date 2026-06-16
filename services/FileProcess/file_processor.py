import pandas as pd


class FileProcessor:

    def read_file(self, file_path):

        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)

        if file_path.endswith(".xlsx"):
            return pd.read_excel(file_path)

        raise ValueError("Unsupported file")

    def clean_dataframe(self, df):

        df = df.fillna("")
        df = df.drop_duplicates()

        return df

    def row_to_text(self, row):

        return f"""
            Product: {row.get('product_name', '')}
            Brand: {row.get('brand', '')}
            Category: {row.get('category', '')}
            Features: {row.get('features', '')}
            Description: {row.get('description', '')}
            Rating: {row.get('rating', '')}
            Stock: {row.get('stock', '')}
            Price: {row.get('price', '')}
            """.strip()

    def process_upload(self, file_path):

        df = self.read_file(file_path)
        df = self.clean_dataframe(df)

        products = []

        for idx, row in df.iterrows():

            row_dict = row.to_dict()

            combined_text = self.row_to_text(row)

            row_dict["combined_text"] = combined_text

            if "product_id" not in row_dict:
                row_dict["product_id"] = idx + 1

            products.append(row_dict)

        return products
