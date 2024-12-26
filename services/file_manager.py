import os
from pathlib import Path
import PyPDF2

class FileManager:
"""
This class manages the uploading,
saving and extracting the content of the
uploaded file that can be later utilized for
RAG
"""
    def __init__(self, upload_dir):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def file_validate(self, file):
        """
        validate if the file is pdf or text file
        Future improvement: allow scanned documents pdf
        """
        return file.content_type in ["application/pdf", "text/plain"]

    async def save_file(self, file):
        """
        async method for I/O operations
        """
        file_path = self.upload_dir / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            return file_path

    def parse_file(self, file_path):
        """
        parse file and extract the content from the pdf/txt file
        """
        ext = file_path.suffix.lower()
        content = ""
        if ext == ".pdf":
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    content+= page.extract_text()
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            raise ValueError("Unsupported file. Only PDF and text file accpeted")
        return content


                
                
                
        

    
    
        