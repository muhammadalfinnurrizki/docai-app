from fastapi import FastAPI, UploadFile, File
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend DocAI berjalan!"}

@app.post("/ocr-pdf/")
async def ocr_pdf(file: UploadFile = File(...)):
    # Baca PDF dengan PyMuPDF
    pdf_bytes = await file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    all_text = ""
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        text = pytesseract.image_to_string(img, lang="eng")
        all_text += f"\n--- Page {page_num+1} ---\n{text}"

    return {"filename": file.filename, "extracted_text": all_text}





