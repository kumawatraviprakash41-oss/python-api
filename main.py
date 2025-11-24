from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from rembg import remove
import io

app = FastAPI()


@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        # Read uploaded file bytes
        input_bytes = await file.read()

        # Remove background using rembg AI
        output_bytes = remove(input_bytes)

        return Response(
            content=output_bytes,
            media_type="image/png",
            headers={"Content-Disposition": "inline; filename=clean.png"}
        )

    except Exception as e:
        return {"error": str(e)}


@app.get("/")
def home():
    return {"message": "AI Background Remove API Working!"}
