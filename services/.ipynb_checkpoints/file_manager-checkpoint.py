import os
from pathlib import Path
import PyPDF2
import chardet
import uuid


class FileManager:
    """
    This class manages the uploading,
    saving and extracting the content of the
    uploaded file that can be later utilized for
    RAG.
    """
    def __init__(self, upload_dir):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def file_validate(self, file):
        """
        Validate if the file is a PDF or text file.
        Future improvement: allow scanned documents (PDF).
        """
        return file.content_type in ["application/pdf", "text/plain"]

    def unique_file_name(self, file):
        """
        Generate a unique file name to prevent overwriting.
        """
        return f"{uuid.uuid4()}_{file.filename}"

    async def save_file(self, file):
        """
        Save the uploaded file asynchronously to the upload directory.
        """
        if not self.file_validate(file):
            raise ValueError("Invalid file type. Only PDF and text files are supported.")

        file_path = self.upload_dir / self.unique_file_name(file)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        return file_path

    def parse_file(self, file_path):
        """
        Parse file and extract the content from the PDF or text file.
        """
        ext = file_path.suffix.lower()
        content = ""

        if ext == ".pdf":
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        content += text
        elif ext == ".txt":
            with open(file_path, "rb") as f:
                raw_data = f.read()
                detected_encoding = chardet.detect(raw_data)['encoding']

            with open(file_path, "r", encoding=detected_encoding) as f:
                content = f.read()
        else:
            raise ValueError("Unsupported file. Only PDF and text files are accepted.")
        
        if not content.strip():
            raise ValueError("File content is empty or could not be extracted.")
        
        return content
