from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Optional
import os
from product_support.main import (
    get_machine_details,
    get_initial_hypothesis,
    call_main_crew,
)


app = FastAPI()

# Allow CORS for frontend local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

QR_UPLOAD_FOLDER = "user_inputs/qr_scan"
IMAGE_UPLOAD_FOLDER = "user_inputs/images"
os.makedirs(QR_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(IMAGE_UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
async def home():
    return {"status": "API is running", "message": "Welcome to Agentic Support!"}


@app.post("/upload_qr_image")
async def upload_qr_image_backend(file: UploadFile):
    global initial_hypothesis, machine_details
    file_location = os.path.join(QR_UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    file_names = [
        f
        for f in os.listdir(QR_UPLOAD_FOLDER)
        if os.path.isfile(os.path.join(QR_UPLOAD_FOLDER, f))
    ]

    if file_names:
        first_file = os.path.join(QR_UPLOAD_FOLDER, file_names[0])
        machine_details = get_machine_details(first_file)
        os.remove(first_file)

    initial_hypothesis = get_initial_hypothesis(machine_details)
    return JSONResponse(content={"suggestions": initial_hypothesis})


@app.post("/upload")
async def upload_image(file: UploadFile):
    file_location = os.path.join(IMAGE_UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"status": "image saved", "filename": file.filename}


@app.post("/chat")
async def chat_with_bot(
    message: Optional[str] = Form(None), file: Optional[UploadFile] = None
):
    conversation_history = []

    # write new images
    if file:
        file_location = os.path.join(IMAGE_UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())

    conversation_history, final_result = call_main_crew(
        message, machine_details, conversation_history
    )

    # delete once done
    for filename in os.listdir(IMAGE_UPLOAD_FOLDER):
        file_path = os.path.join(IMAGE_UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")

    # non api testing
    # import asyncio
    # await asyncio.sleep()

    return JSONResponse(
        content={"message": final_result, "suggestions": initial_hypothesis}
    )
