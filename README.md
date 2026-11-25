
# CloudOps AI Assistant

A lightweight AI chatbot built using Python, FastAPI, Ollama and Qwen 2.5 1.5B.

CloudOps AI Assistant answers general questions and provides technical assistance related to cloud computing, Linux, programming and DevOps.

## Features

- AI-powered conversations
- General question answering
- AWS and Azure assistance
- Linux and DevOps guidance
- Docker and Kubernetes explanations
- Conversation context
- Responsive web interface
- Local AI inference without paid API credits

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| AI Runtime | Ollama |
| AI Model | Qwen 2.5 1.5B |

## Architecture

Browser → FastAPI → Ollama → Qwen 2.5 1.5B

## Project Structure

```text
CloudOps-ai/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.10 or newer
- Git
- Ollama

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/sebin31/CloudOps-ai-assistance.git
cd CloudOps-ai-assistance
```

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r backend/requirements.txt
```

### 5. Download the AI model

```powershell
ollama pull qwen2.5:1.5b
```

### 6. Start the backend

```powershell
cd backend
uvicorn main:app --reload
```

Backend: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

### 7. Start the frontend

Open another terminal:

```powershell
cd frontend
python -m http.server 5500
```

Frontend: http://127.0.0.1:5500

## Future Improvements

- Docker containerization
- AWS EC2 deployment
- Nginx reverse proxy
- GitHub Actions CI/CD

## Author

Sebin Stanley
