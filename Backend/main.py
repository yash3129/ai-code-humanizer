from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from humanizer import humanize_code

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-code-humanizer.vercel.app"],
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