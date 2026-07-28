from langchain_community.document_loaders import Docx2txtLoader


class DOCXLoader:

    def load(self, file_path):
        loader = Docx2txtLoader(file_path)

        documents = loader.load()

        return documents