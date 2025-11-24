from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from PIL import Image
import io

app = FastAPI()

def remove_background_bytes(image_bytes, threshold=200):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            newData.append((255, 255, 255, 0))  # transparent
        else:
            newData.append(item)

    img.putdata(newData)

    # return image as bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    return img_byte_arr.getvalue()


@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    # Read uploaded image from memory
    original_bytes = await file.read()

    # Process background remove (in RAM)
    clean_bytes = remove_background_bytes(original_bytes)

    # Return processed image directly
    return Response(
        content=clean_bytes,
        media_type="image/png",
        headers={"Content-Disposition": "inline; filename=clean.png"}
    )


@app.get("/")
def home():
    return {"message": "Memory-based background remove API working!"}
