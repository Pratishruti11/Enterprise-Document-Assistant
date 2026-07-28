from langchain_chroma import Chroma
from config import VECTOR_DB_PATH


class Retriever:

    def __init__(self, embedding_model):

        self.db = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=embedding_model
        )

    def retrieve(self, query, k=3):
        return self.db.similarity_search(query, k=k)