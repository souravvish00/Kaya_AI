from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..knowledge.document_store import ingest_document, list_chunks, list_documents

router = APIRouter()


@router.get("/documents")
def documents():
    return {"documents": list_documents()}


@router.get("/documents/chunks")
def document_chunks():
    return {"chunks": list_chunks()}


@router.post("/documents/text")
def add_text_document(
    title: str = Form(...),
    text: str = Form(...)
):
    try:
        document = ingest_document(title=title, text=text, source="manual-text")
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return {"document": document}


@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    raw = await file.read()
    text = _decode_text(raw, file.filename or "source")

    try:
        document = ingest_document(title=file.filename or "Uploaded source", text=text, source="upload")
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return {"document": document}


def _decode_text(
    raw: bytes,
    filename: str
) -> str:

    suffix = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""

    if suffix == "pdf":
        try:
            from pypdf import PdfReader
            from io import BytesIO

            reader = PdfReader(BytesIO(raw))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as error:
            raise HTTPException(
                status_code=400,
                detail=f"Could not read PDF text: {error}"
            ) from error

    for encoding in ("utf-8", "utf-16", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue

    raise HTTPException(status_code=400, detail="Unsupported file encoding.")
