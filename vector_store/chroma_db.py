from langchain_chroma import Chroma

from config import CHROMA_DB_PATH


class ChromaVectorStore:

    def __init__(self, embedding_model):

        self.embedding_model = embedding_model

        # Load existing database if available
        self.db = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=self.embedding_model
        )

    # # Used only once (initial database creation)
    # def create_vector_store(self, documents):

    #     self.db.add_documents(documents)

    #     return self.db

    # Used whenever new documents are uploaded
    def add_documents(self, documents):

        self.db.add_documents(documents)

        return self.db

    def get_db(self):

        return self.db