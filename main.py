from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import os
from rembg import remove
from PIL import Image
import uuid

app = FastAPI()

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    try:
        # Unique filename generate
        input_filename = f"{uuid.uuid4()}_{file.filename}"
        output_filename = input_filename.replace(".jpg", ".png").replace(".jpeg", ".png")

        input_path = os.path.join(UPLOAD_FOLDER, input_filename)
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        # Save input image
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # Background remove
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_image.save(output_path)

        return {
            "status": "success",
            "download_url": f"/download/{output_filename}"
        }

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/download/{filename}")
def download_image(filename: str):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    return FileResponse(path=file_path, filename=filename)


@app.get("/")
def home():
    return {"message": "Background Remove API Active!"}
