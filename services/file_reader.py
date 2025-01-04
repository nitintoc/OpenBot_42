import PyPDF2

class FileReader:
    def read_file(self, file):
        """
        Reads a file and returns chunks of text with associated metadata.
        """
        metadata = {"filename": file.filename}
        text_chunks = []

        if file.content_type == "application/pdf":
            reader = PyPDF2.PdfReader(file.file)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                text_chunks.append({"text": text, "metadata": {**metadata, "page_number": i + 1}})
        elif file.content_type == "text/plain":
            text = file.file.read().decode("utf-8")
            text_chunks.append({"text": text, "metadata": metadata})
        else:
            raise ValueError("Unsupported file type")

        return text_chunks
