# Rajeev Portfolio Chatbot API

This is a Python FastAPI backend that runs the portfolio chatbot using the Gemini API.

## Requirements

- Python 3.10+
- Dependencies installed via `uv`

## Setup

1. Copy the `.env.example` or edit the existing `chatbot/.env` file.
2. Set your Google Gemini API Key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Running the API locally

You can run the API backend using:

```bash
uv run uvicorn chatbot.app:app --reload --host 127.0.0.1 --port 8000
```

The server will start at `http://127.0.0.1:8000`.

## Endpoints

- `GET /api/health`: Health status and config check.
- `POST /api/chat`: Chat conversation endpoint.
  - Request body format:
    ```json
    {
      "message": "Hello, tell me about Rajeev.",
      "history": [
        {
          "role": "user",
          "content": "Hi"
        },
        {
          "role": "assistant",
          "content": "Hello! I am Rajeev's virtual AI assistant. How can I help you today?"
        }
      ]
    }
    ```
