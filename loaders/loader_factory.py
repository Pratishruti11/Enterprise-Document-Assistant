import os

from loaders.pdf_loader import PDFLoader
from loaders.docx_loader import DOCXLoader
from loaders.txt_loader import TXTLoader
from loaders.csv_loader import CSVLoader


class LoaderFactory:

    @staticmethod
    def get_loader(file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return PDFLoader()

        elif extension == ".docx":
            return DOCXLoader()

        elif extension == ".txt":
            return TXTLoader()
        
        elif extension == ".csv":
            return CSVLoader()

        else:
            raise ValueError(f"Unsupported file type: {extension}")