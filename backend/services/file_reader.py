import PyPDF2
import logging
import uuid
from typing import List, Dict, Any
import chardet
from fastapi import UploadFile
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileReader:
    async def read_file(self, file: UploadFile) -> List[Dict[str, Any]]:
        """
        Reads a file and returns chunks of text with associated metadata.

        Args:
            file: A FastAPI UploadFile object.

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
            # Reset file pointer to beginning
            await file.seek(0)
            
            if file.content_type == "application/pdf":
                await self._read_pdf(file, metadata, text_chunks)
            elif file.content_type == "text/plain":
                await self._read_text(file, metadata, text_chunks)
            else:
                raise ValueError(f"Unsupported file type: {file.content_type}")
                
            # Reset file pointer again after reading
            await file.seek(0)
            
        except Exception as e:
            logger.error(f"Error reading file {file.filename}: {e}")
            raise

        return text_chunks

    async def _read_pdf(self, file: UploadFile, metadata: Dict[str, Any], text_chunks: List[Dict[str, Any]]):
        """Helper method to extract text from a PDF file."""
        try:
            # Create a copy of the file content to avoid file handle issues
            file_content = await file.read()
            reader = PyPDF2.PdfReader(BytesIO(file_content))
            
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

    async def _read_text(self, file: UploadFile, metadata: Dict[str, Any], text_chunks: List[Dict[str, Any]], chunk_size: int = 1000):
        """Helper method to extract text from a plain text file and split into chunks."""
        try:
            # Read the file content
            file_content = await file.read()
            
            # Detect encoding
            encoding = chardet.detect(file_content)['encoding'] or 'utf-8'
            logger.info(f"Detected encoding for {metadata['filename']}: {encoding}")
            
            # Decode and process text
            text = file_content.decode(encoding).strip()
            
            if not text:
                logger.warning(f"Empty text file: {metadata['filename']}")
                return

            # Split text into smaller chunks for better processing
            for i in range(0, len(text), chunk_size):
                chunk = text[i:i + chunk_size]
                if chunk.strip():  # Only add non-empty chunks
                    text_chunks.append({
                        "text": chunk,
                        "metadata": {**metadata, "chunk_number": i // chunk_size + 1}
                    })

        except UnicodeDecodeError as e:
            logger.error(f"Encoding error in file {metadata['filename']}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error processing text file {metadata['filename']}: {e}")
            raise
