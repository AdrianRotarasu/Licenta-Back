import os
from deeplearning import modify
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH, 'static/upload/')


@app.post("/")
async def index(image: UploadFile = File(...)):
    upload_file = image.file
    filename = image.filename
    path_save = os.path.join(UPLOAD_PATH, filename)
    
    with open(path_save, "wb") as f:
        f.write(upload_file.read())

    text = modify(path_save, filename)
    print(len(text))
    if len(text) < 2:
        text = "No text found"
    return filename


@app.get("/uploads/{filename}")
async def get_uploaded_file(filename):
    return FileResponse(path="static/modified_uploads/" + filename)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)