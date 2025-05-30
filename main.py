from fastapi import FastAPI, UploadFile, File
from typing import List
from fastapi.responses import JSONResponse
from docling.document_converter import DocumentConverter
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

        converter = DocumentConverter()
        result = converter.convert(input_path)

        with open(input_path.replace(".pdf", ".txt"), "w") as f:
            f.write(result.document.export_to_markdown())

    return JSONResponse(
        content={
            "message": "Processamento concluído com sucesso",
            "status": "success"
        },
        status_code=200
    )
