from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
import cv2
import numpy as np
import io
from PIL import Image

app = FastAPI()

def remove_bg_grabcut(image_bytes):
    # Read image
    image = Image.open(io.BytesIO(image_bytes))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2RGB)

    # Create mask
    mask = np.zeros(img.shape[:2], np.uint8)

    # Models for GrabCut
    bgModel = np.zeros((1, 65), np.float64)
    fgModel = np.zeros((1, 65), np.float64)

    # Rectangle roughly containing the subject
    h, w = img.shape[:2]
    rect = (10, 10, w-20, h-20)

    # Apply GrabCut
    cv2.grabCut(img, mask, rect, bgModel, fgModel, 5, cv2.GC_INIT_WITH_RECT)

    # 0 & 2 = background, 1 & 3 = foreground
    mask2 = np.where((mask == 0) | (mask == 2), 0, 1).astype('uint8')

    # Apply mask
    result = img * mask2[:, :, np.newaxis]

    # Convert result to RGBA (transparent bg)
    result_rgba = cv2.cvtColor(result, cv2.COLOR_RGB2RGBA)
    result_rgba[:, :, 3] = mask2 * 255

    # Convert back to bytes
    pil_img = Image.fromarray(result_rgba)
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    return buf.getvalue()


@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    clean = remove_bg_grabcut(image_bytes)

    return Response(
        content=clean,
        media_type="image/png",
        headers={"Content-Disposition": "inline; filename=clean.png"}
    )


@app.get("/")
def home():
    return {"message": "Python GrabCut Background Remove API working!"}
