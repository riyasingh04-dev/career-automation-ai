from pypdf import PdfReader

class PDFParser:
    @staticmethod
    def extract_text(file_path: str) -> str:
        text = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text()
        return text
