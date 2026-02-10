# 🔍 FastAPI Qdrant Semantic Search

A high-performance **Semantic Search Microservice** designed to retrieve documents based on meaning rather than just keyword matching. Built with **FastAPI**, **Qdrant** (Vector Database), and **Sentence Transformers**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-crimson?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## 📖 Overview

Traditional search engines often fail when the user's query doesn't exactly match the keywords in the document. This project solves that problem using **Vector Embeddings**.

It converts text data into high-dimensional vectors using machine learning models (`all-MiniLM-L6-v2`) and stores them in **Qdrant**. This allows the system to understand the *context* and *semantic meaning* behind a user's query.

### Key Features
* **🚀 Neural Search:** Finds relevant results even if no common keywords exist.
* **⚡ Async API:** Built on FastAPI for high concurrency and performance.
* **🐳 Containerized:** Fully dockerized setup (API + Database) for easy deployment.
* **🧠 Automated Vectorization:** Automatically converts text to vectors upon ingestion.
* **💾 Persistent Storage:** Data persists across container restarts via Docker Volumes.

---

## 🏗 Architecture

1.  **Client** sends a text document to the API.
2.  **FastAPI Service** uses `SentenceTransformer` to convert text -> Vector (384 dimensions).
3.  **Qdrant** stores the Vector + Original Text (Payload).
4.  **Search:** When a user queries, the query is vectorized, and Qdrant finds the nearest neighbors using Cosine Similarity.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10
* **Web Framework:** FastAPI + Uvicorn
* **Vector Database:** Qdrant
* **ML Model:** `sentence-transformers/all-MiniLM-L6-v2`
* **Infrastructure:** Docker & Docker Compose

---

## 🚀 Getting Started

### Prerequisites
* Docker & Docker Compose installed.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/fastapi-qdrant-search.git](https://github.com/your-username/fastapi-qdrant-search.git)
    cd fastapi-qdrant-search
    ```

2.  **Start the services:**
    This command will download the ML models, build the API container, and start the Database.
    ```bash
    docker-compose up --build -d
    ```

3.  **Access the API:**
    * **Swagger UI (Documentation):** [http://localhost:8000/docs](http://localhost:8000/docs)
    * **Qdrant Dashboard:** [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

---

## 🔌 API Usage Examples

### 1. Ingest Documents (Indexing)
Upload text data to the vector database.

**POST** `/api/v1/ingest`
```json
[
  {
    "text": "FastAPI is a modern web framework for building APIs with Python.",
    "metadata": {"category": "tech"}
  },
  {
    "text": "The quick brown fox jumps over the lazy dog.",
    "metadata": {"category": "animals"}
  }
]