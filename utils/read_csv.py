import pandas as pd


class FileProcessor:
    def read_file(self, file_path):
        """Read CSV or Excel file."""

        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)

        if file_path.endswith(".xlsx"):
            return pd.read_excel(file_path)

        raise ValueError("Unsupported file type")

    def clean_dataframe(self, df):
        """Remove null values and duplicates."""

        df = df.fillna("")
        df = df.drop_duplicates()

        return df

    def row_to_text(self, row):
        """Convert dataframe row into text."""

        return " | ".join(
            f"{column}: {value}"
            for column, value in row.items()
            if str(value).strip()
        )

    def process_upload(self, file_path):
        """Read file and convert rows into text."""

        df = self.read_file(file_path)
        df = self.clean_dataframe(df)

        documents = []

        for _, row in df.iterrows():
            text = self.row_to_text(row)

            if text:
                documents.append(text)

        return documents
