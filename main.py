from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from PIL import Image
import io

app = FastAPI()

def remove_background_bytes(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

    datas = img.getdata()
    newData = []

    # White/light background remove
    for item in datas:
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    return buffer.getvalue()


@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        clean = remove_background_bytes(image_bytes)

        return Response(
            clean,
            media_type="image/png",
            headers={"Content-Disposition": "inline; filename=clean.png"}
        )

    except Exception as e:
        return {"error": str(e)}


@app.get("/")
def home():
    return {"message": "Background remove API working!"}
