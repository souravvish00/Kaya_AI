# 🚀 KAYA AI

KAYA is a local AI assistant built with FastAPI and React. It is designed to learn from documents, remember important information, analyze uploaded content, and provide intelligent responses using local or external language models.

## Features

* 💬 AI Chat Assistant
* 🧠 Long-Term Memory System
* 📚 Document Learning (PDF, TXT, DOCX)
* 🖼️ Image OCR Support
* 🔍 Knowledge Retrieval
* 🧮 Built-in Calculator
* 📊 Training Dataset Management
* 🤖 Ollama Integration
* 📝 Automatic Summarization
* 🎯 Conclusion Generation

---

## Tech Stack

### Backend

* Python
* FastAPI
* Pydantic
* Ollama
* ChromaDB (recommended)
* PyPDF
* Python-Docx
* Pillow
* Pytesseract

### Frontend

* React
* Vite
* JavaScript
* CSS

---

## Project Structure

```text
KAYA/
├── backend/
│   ├── api/
│   ├── llm/
│   ├── memory/
│   ├── knowledge/
│   ├── training/
│   ├── tools/
│   └── database/
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── services/
│   │   └── utils/
│   └── public/
│
├── uploads/
├── logs/
├── data/
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd KAYA
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\\Scripts\\activate
```

Linux / Mac:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

---

## Running KAYA

### Backend

```bash
uvicorn backend.app.main:app --reload
```

### Frontend

```bash
npm run dev
```

---

## Ollama Setup

Install Ollama:

https://ollama.com/download

Download model:

```bash
ollama pull qwen2.5:7b
```

Run model:

```bash
ollama run qwen2.5:7b
```

---

## Future Roadmap

* ChromaDB Integration
* Advanced Memory Retrieval
* Cybersecurity Knowledge Base
* Fine-Tuned KAYA Model
* Image Understanding
* Voice Assistant
* Autonomous Learning Workflows

---

## Author

**Sourav Vishwakrma**

Building KAYA AI – a local learning and knowledge assistant designed for intelligent document understanding, memory, and personalized AI experiences.
