# aiMovieChatbot

API Documentation: [aiMovieChatbot API](https://aimoviebot.devrohit.tech/)

## Overview
aiMovieChatbot is a multi-level REST API chatbot that allows users to interact with movie characters, retrieve movie scripts, and perform semantic searches using advanced AI techniques.

## Running Locally

### 1. Create a `.env` file in the backend root directory
Add the following environment variables:
```env
REDIS_URL=redis://127.0.0.1:6379
ORIGINS=http://localhost:8000
QDRANT_URI=http://localhost:6333
PSQL_URI=postgres://myuser:mypassword@127.0.0.1:5432/mydatabase
```

### 2. Get Google Vertex AI API Key
Follow the instructions here: [Google Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstarts/quickstart-multimodal)
- Download the JSON key file and store it on your local device.

### 3. Start Backend Services
Navigate to the backend folder and run the following command to start Redis, PostgreSQL, and Qdrant using Docker:
```sh
docker compose up -d
```

### 4. Set Up Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Set Google API Credentials
Replace `key.json` with your actual Google Vertex AI API key file path:
```sh
export GOOGLE_APPLICATION_CREDENTIALS='key.json'
```

### 6. Run the Server
This process will take approximately 15-20 minutes to scrape data and create embeddings in QdrantDB. Once completed, the server will start automatically.
```sh
fastapi dev main.py 
```

Visit: [http://localhost:8000/](http://localhost:8000/)

