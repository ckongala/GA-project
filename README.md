<div align="center">

# 🧠 NLP Text Analysis API

### *Intelligent Text & Video Content Analysis Microservices*

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.2.3-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![Hugging Face](https://img.shields.io/badge/🤗_Hugging_Face-Transformers-FFD21E?style=for-the-badge)](https://huggingface.co)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3_|_Whisper-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

<br/>

**Production-ready RESTful API for advanced NLP tasks including toxicity detection, emotion classification, moral foundation analysis, and YouTube video content processing.**

[Features](#-features) •
[Quick Start](#-quick-start) •
[API Reference](#-api-reference) •
[Examples](#-usage-examples) •
[Deployment](#-deployment)

---

</div>

## 📑 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [API Reference](#-api-reference)
- [Usage Examples](#-usage-examples)
- [Deployment](#-deployment)
- [Performance](#-performance)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📝 Text Analysis

| Feature | Description |
|:--------|:------------|
| 🔴 **Toxicity Detection** | Multi-label classification for toxic content |
| 💭 **Sentiment Analysis** | Polarity scoring (-1 to +1) |
| 😊 **Emotion Detection** | 7 emotion categories |
| ⚖️ **Morality Analysis** | Moral Foundations Theory scoring |

</td>
<td width="50%">

### 🎬 YouTube Analysis

| Feature | Description |
|:--------|:------------|
| 📜 **Transcription** | Auto-fetch with Whisper fallback |
| 🌍 **Translation** | Multi-language support |
| 📰 **Narrative Extraction** | GPT-3 powered headlines |
| 🎨 **Video Barcode** | Visual color fingerprint |

</td>
</tr>
</table>

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              CLIENT REQUEST                              │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          🔒 AUTH VALIDATOR                               │
│                      Request Validation Layer                            │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│   │  /toxicity   │  │  /emotion    │  │  /morality   │  │  /youtube  │  │
│   │  Controller  │  │  Controller  │  │  Controller  │  │ Controllers│  │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘  │
│          │                 │                 │                │         │
│   ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐  ┌─────▼──────┐  │
│   │   Toxicity   │  │   Emotion    │  │   Morality   │  │  YouTube   │  │
│   │   Service    │  │   Service    │  │   Service    │  │  Services  │  │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘  │
│          │                 │                 │                │         │
│   ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐  ┌─────▼──────┐  │
│   │   Detoxify   │  │DistilRoBERTa │  │  emfdscore   │  │GPT-3/Whisper│ │
│   │    Model     │  │    Model     │  │   Library    │  │  /OpenCV   │  │
│   └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
│                                                                          │
│                         📊 FLASK APPLICATION                             │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   📈 StatsD      │  │   🗄️ MySQL       │  │   📁 SFTP        │
│   Monitoring     │  │   Database       │  │   Storage        │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

---

## 🛠 Tech Stack

<table>
<tr>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=python" width="48" height="48" alt="Python" />
<br>Python 3.10
</td>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=flask" width="48" height="48" alt="Flask" />
<br>Flask
</td>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=pytorch" width="48" height="48" alt="PyTorch" />
<br>PyTorch
</td>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=docker" width="48" height="48" alt="Docker" />
<br>Docker
</td>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=mysql" width="48" height="48" alt="MySQL" />
<br>MySQL
</td>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=opencv" width="48" height="48" alt="OpenCV" />
<br>OpenCV
</td>
</tr>
</table>

### Core Dependencies

| Category | Libraries |
|:---------|:----------|
| **ML/NLP** | `transformers` `detoxify` `spacy` `nltk` `textblob` `emfdscore` |
| **AI APIs** | `openai` (GPT-3, Whisper) |
| **Video** | `opencv-python` `ffmpeg-python` `pytube` `imutils` |
| **Web** | `flask` `flask-restful` `flask-swagger-ui` |
| **Data** | `pandas` `numpy` `scikit-learn` |

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version | Notes |
|:------------|:--------|:------|
| Python | 3.10.x | Required |
| ffmpeg | Latest | For audio/video processing |
| CUDA | 11.x+ | Optional (GPU acceleration) |

### Installation

<details>
<summary><b>🍎 macOS</b></summary>

```bash
# Install ffmpeg
brew install ffmpeg

# Clone & setup
git clone <repository-url>
cd GA-project

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

</details>

<details>
<summary><b>🐧 Linux (Ubuntu/Debian)</b></summary>

```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3.10 python3.10-venv ffmpeg libgl1

# Clone & setup
git clone <repository-url>
cd GA-project

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

</details>

<details>
<summary><b>🪟 Windows</b></summary>

```powershell
# Install ffmpeg via chocolatey
choco install ffmpeg

# Clone & setup
git clone <repository-url>
cd GA-project

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

</details>

### Run the Server

```bash
# Development mode
flask --app src/app run --port 5001

# Or use the script
./flask-run.sh
```

<div align="center">

🎉 **API is now running at** `http://localhost:5001`

📚 **Swagger UI available at** `http://localhost:5001/swagger`

</div>

---

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
# ═══════════════════════════════════════════════════════════
#                    REQUIRED CONFIGURATIONS
# ═══════════════════════════════════════════════════════════

# OpenAI API (Required for GPT-3 and Whisper features)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ═══════════════════════════════════════════════════════════
#                    OPTIONAL CONFIGURATIONS
# ═══════════════════════════════════════════════════════════

# MySQL Database
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=nlp_api

# SFTP Storage (for barcode uploads)
BARCODE_FTP_HOST=your.sftp.host
BARCODE_FTP_USERNAME=your_username
BARCODE_FTP_PASSWORD=your_password

# StatsD Monitoring
STATSD_HOST=localhost
STATSD_PORT=8125
```

---

## 📖 API Reference

### Base URL
```
http://localhost:5001/api/v1
```

### Endpoints Overview

| Status | Method | Endpoint | Description |
|:------:|:------:|:---------|:------------|
| 🟢 | `GET` | `/ping/` | Health check |
| 🔴 | `POST` | `/toxicity/` | Toxicity & sentiment analysis |
| 😊 | `POST` | `/emotion/` | Emotion detection |
| ⚖️ | `POST` | `/morality/` | Moral foundations scoring |
| 📜 | `POST` | `/youtube/transcript/` | Video transcription |
| 📰 | `POST` | `/youtube/gpt3_narrative/` | GPT-3 narrative generation |
| 🔑 | `POST` | `/youtube/gpt3_keywords/` | GPT-3 keyword extraction |
| ✂️ | `POST` | `/youtube/chunk-transcripts/` | Transcript chunking |
| 📊 | `POST` | `/youtube/tfidf-narrative/` | TF-IDF narrative extraction |
| 🎨 | `POST` | `/youtube/generate-barcode` | Video barcode generation |

---

## 💡 Usage Examples

### 🔴 Toxicity Detection

Analyze text for harmful content with optional sentiment scoring.

<table>
<tr>
<td width="50%">

**Request**
```bash
curl -X POST http://localhost:5001/api/v1/toxicity/ \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"text": "You are amazing!"},
      {"text": "I hate everything about this."}
    ],
    "process_sentiment": true
  }'
```

</td>
<td width="50%">

**Response**
```json
[
  {
    "toxicity": 0.0008,
    "severe_toxicity": 0.0001,
    "obscene": 0.0002,
    "threat": 0.0001,
    "insult": 0.0003,
    "identity_attack": 0.0001,
    "sentiment": 0.85
  },
  {
    "toxicity": 0.8542,
    "severe_toxicity": 0.0124,
    "obscene": 0.1203,
    "threat": 0.0089,
    "insult": 0.7234,
    "identity_attack": 0.0156,
    "sentiment": -0.72
  }
]
```

</td>
</tr>
</table>

---

### 😊 Emotion Detection

Classify text into one of 7 emotions with confidence scores.

<table>
<tr>
<td width="50%">

**Request**
```bash
curl -X POST http://localhost:5001/api/v1/emotion/ \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"text": "This is the best day ever!"},
      {"text": "I cannot believe they did that."},
      {"text": "The meeting is at 3pm."}
    ]
  }'
```

</td>
<td width="50%">

**Response**
```json
[
  {"emotion": "joy", "score": 0.9834},
  {"emotion": "surprise", "score": 0.7621},
  {"emotion": "neutral", "score": 0.9156}
]
```

**Emotion Categories:**
- 😠 `anger`
- 🤢 `disgust`
- 😨 `fear`
- 😊 `joy`
- 😐 `neutral`
- 😢 `sadness`
- 😲 `surprise`

</td>
</tr>
</table>

---

### ⚖️ Morality Analysis

Score text based on Moral Foundations Theory.

<table>
<tr>
<td width="50%">

**Request**
```bash
curl -X POST http://localhost:5001/api/v1/morality/ \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "text": "We must protect the vulnerable.",
        "url": "doc-001"
      }
    ]
  }'
```

</td>
<td width="50%">

**Response**
```json
[
  {
    "url": "doc-001",
    "morality": {
      "Care": 0.423,
      "Fairness": 0.156,
      "Loyality": 0.089,
      "Authority": 0.112,
      "Sanctity": 0.067,
      "Harm": 0.034,
      "Cheating": 0.012,
      "Betrayal": 0.008,
      "Subversion": 0.023,
      "Degradation": 0.015,
      "moral_nonmoral_ratio": 0.72,
      "f_var": 0.045
    }
  }
]
```

</td>
</tr>
</table>

---

### 📜 YouTube Transcript Extraction

Fetch video transcripts with automatic Whisper fallback.

```bash
curl -X POST http://localhost:5001/api/v1/youtube/transcript/ \
  -H "Content-Type: application/json" \
  -d '{
    "video_ids": ["dQw4w9WgXcQ", "oHg5SJYRHA0"]
  }'
```

**Response:**
```json
[
  {
    "video_id": "dQw4w9WgXcQ",
    "transcript": "We're no strangers to love, you know the rules..."
  },
  {
    "video_id": "oHg5SJYRHA0",
    "transcript": "Never gonna give you up, never gonna let you down..."
  }
]
```

---

### 🎨 Video Barcode Generation

Generate a visual color barcode from video frames.

```bash
curl -X POST http://localhost:5001/api/v1/youtube/generate-barcode \
  -H "Content-Type: application/json" \
  -d '{
    "video_ids": ["dQw4w9WgXcQ"]
  }'
```

---

## 🐳 Deployment

### Docker

```bash
# Build image
docker build -t nlp-api:latest .

# Run container
docker run -d \
  --name nlp-api \
  -p 5001:5001 \
  --env-file .env \
  --gpus all \  # Optional: for GPU support
  nlp-api:latest

# View logs
docker logs -f nlp-api
```

### Docker Compose (Recommended)

```yaml
version: '3.8'
services:
  nlp-api:
    build: .
    ports:
      - "5001:5001"
    env_file:
      - .env
    volumes:
      - ./data:/src/data
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
```

---

## ⚡ Performance

### Hardware Recommendations

| Workload | CPU | RAM | GPU |
|:---------|:----|:----|:----|
| Light (< 100 req/hr) | 2 cores | 4 GB | Not required |
| Medium (< 1000 req/hr) | 4 cores | 8 GB | Recommended |
| Heavy (> 1000 req/hr) | 8+ cores | 16+ GB | Required |

### Optimization Tips

- **GPU Acceleration**: All PyTorch models auto-detect and use CUDA when available
- **Batch Processing**: Send multiple texts in a single request for better throughput
- **Chunking**: Use `/chunk-transcripts/` to split long texts (default: 800 words)

---

## 🔧 Troubleshooting

<details>
<summary><b>🚫 CUDA/GPU not detected</b></summary>

```bash
# Verify CUDA installation
python -c "import torch; print(torch.cuda.is_available())"

# Should output: True
# If False, reinstall PyTorch with CUDA:
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

</details>

<details>
<summary><b>🚫 ffmpeg not found</b></summary>

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

</details>

<details>
<summary><b>🚫 YouTube transcript not available</b></summary>

The API automatically falls back to OpenAI Whisper when YouTube transcripts are unavailable. Ensure:
- `OPENAI_API_KEY` is set in `.env`
- Video is publicly accessible
- Video has audio content

</details>

<details>
<summary><b>🚫 Model loading slow on first request</b></summary>

Models are loaded lazily on first request. Subsequent requests will be faster. Consider:
- Pre-warming the API with a test request after startup
- Using a larger instance with more RAM
- Implementing model caching

</details>

---

## 📁 Project Structure

```
GA-project/
├── 📄 main.py                  # Entry point
├── 📄 Dockerfile               # Container configuration
├── 📄 requirements.txt         # Python dependencies
├── 📄 swagger.json             # OpenAPI specification
├── 📄 flask-run.sh             # Run script
│
└── 📁 src/
    ├── 📄 app.py               # Flask app initialization
    │
    ├── 📁 adapters/            # External integrations
    │   ├── statsd_adapter.py
    │   └── universal_data_encoder.py
    │
    ├── 📁 controllers/         # Route handlers
    │   ├── ping_controller.py
    │   ├── toxicity_controller.py
    │   ├── emotion_controller.py
    │   ├── morality_controller.py
    │   └── 📁 youtube/
    │       ├── transcript_controller.py
    │       ├── barcode_controller.py
    │       └── ...
    │
    ├── 📁 services/            # Business logic
    │   ├── toxicity_service.py
    │   ├── emotion_service.py
    │   ├── morality_service.py
    │   └── 📁 youtube/
    │       ├── transcript_service.py
    │       ├── speech_to_text_service.py
    │       └── ...
    │
    ├── 📁 models/              # Request/Response schemas
    ├── 📁 validators/          # Input validation
    ├── 📁 constants/           # Configuration constants
    ├── 📁 exceptions/          # Custom exceptions
    └── 📁 utils/               # Helper utilities
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/awesome-feature
   ```
3. **Commit** your changes
   ```bash
   git commit -m "feat: add awesome feature"
   ```
4. **Push** to your branch
   ```bash
   git push origin feature/awesome-feature
   ```
5. **Open** a Pull Request

### Commit Convention

| Type | Description |
|:-----|:------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `refactor` | Code refactoring |
| `test` | Tests |

---

## 📚 References

- [Detoxify - Toxic Comment Classification](https://github.com/unitaryai/detoxify)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [Moral Foundations Theory](https://moralfoundations.org/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Flask-RESTful Documentation](https://flask-restful.readthedocs.io/)

---

<div align="center">

## ⭐ Star this repo if you find it useful!

<br>

**Built with ❤️ for NLP enthusiasts**

<sub>Developed for intelligent text and video content analysis</sub>

</div>
