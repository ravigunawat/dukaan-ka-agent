from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
from database import init_db, update_stock, get_all_stock
from extract import extract_stock_info
import shutil
import os

load_dotenv()

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "Dukaan ka Agent backend chal raha hai"}

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"error": "OPENAI_API_KEY set nahi hai .env file me"}

    client = OpenAI(api_key=api_key)

    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(temp_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="hi"
        )

    os.remove(temp_path)

    extracted = extract_stock_info(transcript.text)
    update_stock(
        item=extracted["item"],
        quantity=extracted["quantity"],
        unit=extracted.get("unit"),
        price=extracted.get("price"),
        action=extracted["action"]
    )

    return {
        "transcription": transcript.text,
        "extracted": extracted
    }

@app.get("/stock")
def get_stock():
    return {"stock": get_all_stock()}

@app.post("/test-extract")
async def test_extract(text: str):
    extracted = extract_stock_info(text)
    update_stock(
        item=extracted["item"],
        quantity=extracted["quantity"],
        unit=extracted.get("unit"),
        price=extracted.get("price"),
        action=extracted["action"]
    )
    return {"extracted": extracted}
