import io
from fastapi import UploadFile, HTTPException
from pypdf import PdfReader


async def load_document_text(file: UploadFile) -> str:
    """
    Load text from an uploaded legal document (PDF or plain text).
    """
    filename = file.filename.lower()

    try:
        if filename.endswith(".pdf"):
            # Read PDF
            pdf_bytes = await file.read()
            reader = PdfReader(io.BytesIO(pdf_bytes))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        elif filename.endswith(".txt"):
            # Read text file
            text = (await file.read()).decode("utf-8")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Use PDF or TXT.")
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No readable text found in document.")
        
        return text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading document: {e}")
