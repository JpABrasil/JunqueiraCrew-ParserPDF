from fastapi import FastAPI, UploadFile, File
from typing import List
from fastapi.responses import JSONResponse
#from docling.document_converter import DocumentConverter
import pdfplumber 
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

@app.get("/health")
def health():
    return "OK", 200

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou restrinja ex.: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/processar")
async def processar_pdf(files: List[UploadFile] = File(...)) -> JSONResponse:
    saved_files = []

    for file in files:
        filename = file.filename.lower()

        # Salvar o arquivo
        input_path = os.path.join("./uploads", filename)
        os.makedirs("./uploads", exist_ok=True)

        contents = await file.read()

        with open(input_path, "wb") as f:
            f.write(contents)

        #converter = DocumentConverter()
        #result = converter.convert(input_path)
        #with open(input_path.replace(".pdf", ".txt"), "w") as f:
            #f.write(result.document.export_to_markdown())
        
        with pdfplumber.open(input_path) as pdf:
            texto = ""
            for page in pdf.pages:
                texto += (page.extract_text() or "") + "\n"  # Garante que não quebre se a página não tiver texto

        with open(input_path.replace(".pdf", ".txt"), "w", encoding="utf-8") as f:
            f.write(texto)

    return JSONResponse(
        content={
            "message": texto,
            "status": "success"
        },
        status_code=200
    )
