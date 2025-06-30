from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Permetti CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Static frontend
frontend_path = r"C:\Users\butterfly\Desktop\ciao\MAGISTRALE\AI\llama3\src\frontend"
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Serve la pagina principale
@app.get("/")
def serve_index():
    index_path = os.path.join(frontend_path, "index.html")
    return FileResponse(index_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
