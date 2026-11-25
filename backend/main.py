import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal


# Ollama configuration
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://127.0.0.1:11434/api/chat"
)

MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5:1.5b"
)

app = FastAPI(title="CloudOps AI Assistant")


# Allow the local frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# Chat message format
class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "CloudOps AI Assistant is running!"
    }


# Chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):

    if not request.messages:
        raise HTTPException(
            status_code=400,
            detail="Please enter a message."
        )

    if len(request.messages) > 30:
        raise HTTPException(
            status_code=400,
            detail="Conversation too long. Start a new chat."
        )

    if request.messages[-1].role != "user":
        raise HTTPException(
            status_code=400,
            detail="Latest message must be from the user."
        )

    # Prepare conversation history
    messages = [
        {
            "role": "system",
            "content": """
            You are CloudOps AI Assistant.

            You are a friendly and knowledgeable AI assistant.

            Answer general questions and technical questions
            about AWS, Azure, Linux, Docker, Kubernetes,
            Python, networking and DevOps.

            Explain concepts in simple language.
            Provide practical examples and commands when useful.
            Warn users before suggesting destructive commands.

            Never claim to have executed commands or modified
            infrastructure. You only provide guidance.
            """
        }
    ]

    for message in request.messages:

        if not message.content.strip():
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty."
            )

        if len(message.content) > 10000:
            raise HTTPException(
                status_code=400,
                detail="Message is too long."
            )

        messages.append({
            "role": message.role,
            "content": message.content
        })

    # Prepare Ollama API request
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }

    body = json.dumps(payload).encode("utf-8")

    ollama_request = Request(
        OLLAMA_URL,
        data=body,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:

        with urlopen(ollama_request, timeout=180) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        reply = result.get("message", {}).get("content", "").strip()

        if not reply:
            raise HTTPException(
                status_code=502,
                detail="Ollama returned an empty response."
            )

        return {
            "reply": reply
        }

    except HTTPError as error:

        error_message = error.read().decode(
            "utf-8", errors="replace"
        )

        print("Ollama API error:", error_message)

        raise HTTPException(
            status_code=502,
            detail="Ollama returned an API error."
        )

    except URLError as error:

        print("Ollama connection error:", error)

        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Make sure Ollama is running."
        )

    except TimeoutError:

        raise HTTPException(
            status_code=504,
            detail="Ollama request timed out. Please try again."
        )

