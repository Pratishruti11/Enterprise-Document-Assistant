import pandas as pd
from langchain_core.documents import Document


class CSVLoader:

    def load(self, file_path):

        df = pd.read_csv(file_path)

        documents = []

        for index, row in df.iterrows():

            # Convert the entire row into text
            row_text = "\n".join(
                [f"{column}: {row[column]}" for column in df.columns]
            )

            documents.append(
                Document(
                    page_content=row_text,
                    metadata={
                        "source": file_path,
                        "row": index
                    }
                )
            )

        return documents