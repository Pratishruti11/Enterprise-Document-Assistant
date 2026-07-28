from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:

    def load(self, file_path):
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        return documents