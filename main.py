from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from PIL import Image
import os
import uuid

app = FastAPI()

UPLOAD = "uploads"
OUTPUT = "output"

# Create folders if not exist
os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)


def remove_background(input_path, output_path, threshold=200):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            newData.append((255, 255, 255, 0))  # transparent
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(output_path, "PNG")


@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    input_path = f"{UPLOAD}/{file_id}_{file.filename}"
    output_path = f"{OUTPUT}/{file_id}.png"

    # Save image
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Remove background
    remove_background(input_path, output_path)

    return FileResponse(output_path, media_type="image/png", filename="clean.png")


@app.get("/")
def home():
    return {"message": "Python background remove API working!"}
