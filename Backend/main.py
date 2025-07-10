from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from humanizer import humanize_code

app = FastAPI()

origins = [
    "https://ai-code-humanizer.vercel.app",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    language: str

@app.post("/humanize")
def humanize_endpoint(request: CodeRequest):
    result = humanize_code(request.code, request.language)
    return {
        "original_code": request.code,
        "humanized_code": result
    }