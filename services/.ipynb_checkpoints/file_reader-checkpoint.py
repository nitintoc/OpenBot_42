import PyPDF2
import logging
import uuid
from typing import List, Dict, Any
import chardet

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileReader:
    def read_file(self, file) -> List[Dict[str, Any]]:
        """
        Reads a file and returns chunks of text with associated metadata.

        Args:
            file: A file-like object with 'filename' and 'content_type' attributes.

        Returns:
            A list of dictionaries containing text chunks and metadata.
        """
        file_id = str(uuid.uuid4())  # Generate a unique ID for each file
        metadata = {
            "file_id": file_id,
            "filename": file.filename
        }
        text_chunks = []

        try:
            if file.content_type == "application/pdf":
                self._read_pdf(file, metadata, text_chunks)
            elif file.content_type == "text/plain":
                self._read_text(file, metadata, text_chunks)
            else:
                raise ValueError(f"Unsupported file type: {file.content_type}")
        except Exception as e:
            logger.error(f"Error reading file {file.filename}: {e}")
            raise

        return text_chunks

    def _read_pdf(self, file, metadata, text_chunks):
        """Helper method to extract text from a PDF file."""
        try:
            reader = PyPDF2.PdfReader(file.file)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:  # Skip empty pages
                    text_chunks.append({
                        "text": text.strip(),
                        "metadata": {**metadata, "page_number": i + 1}
                    })
                else:
                    logger.warning(f"Empty or non-extractable text on page {i + 1}")
        except Exception as e:
            logger.error(f"Error processing PDF file {metadata['filename']}: {e}")
            raise

    def _read_text(self, file, metadata, text_chunks, chunk_size=1000):
        """Helper method to extract text from a plain text file and split into chunks."""
        try:
            raw_data = file.file.read()
            encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'  # Auto-detect encoding
            text = raw_data.decode(encoding).strip()

            # Split text into smaller chunks for better processing
            for i in range(0, len(text), chunk_size):
                text_chunks.append({
                    "text": text[i:i + chunk_size],
                    "metadata": {**metadata, "chunk_number": i // chunk_size + 1}
                })

        except UnicodeDecodeError as e:
            logger.error(f"Encoding error in file {metadata['filename']}: {e}")
            raise
