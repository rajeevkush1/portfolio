import json
import os
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from chatbot.tools import scrape_my_profiles

# Load environment variables from chatbot/.env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

app = FastAPI(title="Rajeev Kushwaha Portfolio Chatbot API")

# Configure CORS so the static frontend can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict to portfolio domain if desired
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tool schema definition for Groq OpenAI tool calling
SCRAPE_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "scrape_my_profiles",
        "description": "Scrapes Rajeev's personal profiles (github or kaggle) to retrieve up-to-date live information.",
        "parameters": {
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "description": "The profile platform to scrape. Must be 'github' or 'kaggle'.",
                    "enum": ["github", "kaggle"]
                }
            },
            "required": ["platform"]
        }
    }
}


# Pydantic models for request/response validation
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str

SYSTEM_INSTRUCTION = """
You are "Rajeev's Virtual Assistant", a friendly, professional, and knowledgeable AI chatbot built by Rajeev Kushwaha.
Your goal is to answer questions about Rajeev's professional background, skills, education, projects, and contact info, helping recruiters and visitors learn more about him.

Here are the details of Rajeev's professional profile:

1. PERSONAL SUMMARY:
- Rajeev Kushwaha is an aspiring Machine Learning Engineer & Deep Learning Enthusiast.
- He leverages Python, PyTorch, and cloud platforms to build robust, scalable AI solutions for real-world applications.
- He has a strong foundation in deploying scalable AI solutions using Docker, FastAPI, and cloud platforms.

2. TECHNICAL SKILLS:
- Languages: Python, C, C++, SQL
- AI / ML: Machine Learning, Deep Learning, NLP, Generative AI, Agentic AI, AI Agents, Transformer & LLM Fine-Tuning (LoRA/QLoRA), LangChain, LangGraph, Pydantic, RAG Systems
- Frameworks & Libraries: PyTorch, TensorFlow, Scikit-Learn, Pandas, FastAPI, Flask, Unsloth, BeautifulSoup
- Developer Tools & Infra: Docker, GitHub, Git, MongoDB Atlas, Qdrant (Vector DB), Ollama, REST APIs
- CS Fundamentals: DSA, DBMS, OOP, Operating Systems, Algorithms & System Design
- AI-Assisted Dev: Claude, GitHub Copilot, ChatGPT for coding, debugging, automation, and rapid prototyping


3. PROJECTS:
- Advanced Agentic RAG Pipeline for AI Research Papers: Production-style RAG system with Nougat OCR / pymupdf4llm parsing, hybrid dense-sparse retrieval (BGE-M3/FastEmbed + BM25 with Reciprocal Rank Fusion over Qdrant), and LangGraph ReAct agent loop with adaptive multi-LLM routing. GitHub: https://github.com/rajeevkush1/ragAPI | https://github.com/rajeevkush1/rag-advanced-research
- AI Resume Checker & ATS Scanner: Intelligent ATS resume scanner web app scoring fit via keyword matching (spaCy) and semantic similarity (Sentence-Transformers). Features composite scoring, Streamlit UI, Docker containerization, and Unsloth LoRA fine-tuning. GitHub: https://github.com/rajeevkush1/resume-archietecture/tree/main/resume-checker
- NLP Text Summarization Pipeline: Fine-tuned Hugging Face Transformer model (ROUGE/SacreBLEU evaluation) achieving 88% accuracy for abstractive summarization. Containerized with Docker and served via FastAPI. GitHub: https://github.com/rajeevkush1/TEXT-summarizer-project
- Minesweeper RL Agent (AMD Hackathon, IIT Delhi 2024): Trained a Minesweeper-playing agent using GRPOTrainer with custom reward shaping on Vertex AI Workbench.
- Student Marks Prediction Pipeline: End-to-end ML pipeline with data preprocessing, model training, and FastAPI deployment (R² score of 0.87). GitHub: https://github.com/rajeevkush1/mathsmarks

4. EDUCATION:
- B.Tech in Computer Science (Specialization in Artificial Intelligence & Machine Learning) at GL Bajaj Institute of Technology & Management (Jan 2023 - Dec 2027) | GPA: 7.48 | Media Head, Abhyudaya Club.
- Class XII (PCM) from Delhi Public School - India (2020 - 2022) | Score: 81.2%.
- Class X from Bhartiyam Vidhya Peeth (2019 - 2020) | Score: 97.3%.

5. CERTIFICATIONS & ACHIEVEMENTS:
- Google Cloud Skill Badges (Google Cloud, Silver League - 3272 pts, 7 Badges earned in PMLE, MLOps, LLMs, GenAI)
- Generative AI and ChatGPT (GeeksforGeeks, Nov 2025 - Present)
- Mastering Data Transformation through NLP (GeeksforGeeks, Oct 2025 - Present)
- Intro to Machine Learning (Kaggle, Feb 2025 - Present)
- Pandas (Kaggle, Feb 2025 - Present)

6. CONTACT INFO:
- Phone: +91-7489502973
- Email: rajeev102003000@gmail.com
- GitHub: https://github.com/rajeevkush1
- LinkedIn: https://www.linkedin.com/in/rajeev-kushwaha-578b4b242/
- Kaggle: https://www.kaggle.com/rajeevkushwaha
- Instagram: https://www.instagram.com/rajeevkuxhh_?igsh=MWowMDQzYXQwanl4cQ==
- Location: Greater Noida, India

GUIDELINES FOR YOUR RESPONSES:

- Respond as his virtual AI assistant. Keep responses relatively concise and focused on Rajeev's background, skills, and projects. Don't make up any facts.
- Do NOT pretend to be Rajeev. State that you are his virtual AI assistant. Refer to Rajeev as "Rajeev".
- If asked about something not in his portfolio or resume, politely state: "I don't have that information about Rajeev in my database. Feel free to contact him directly at rajeev102003000@gmail.com or connect via LinkedIn."
- Keep responses professional, helpful, and optimistic. Format key words in bold and use bullet points for lists.
"""

@app.get("/api/health")
def health_check():
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY")
    api_key_status = "configured" if api_key else "missing"
    return {
        "status": "healthy",
        "provider": "Groq",
        "model": "llama-3.3-70b-versatile",
        "api_key": api_key_status
    }

@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is not configured on the server. Please add it to chatbot/.env file."
        )
    
    try:
        # Initialize OpenAI client with Groq's OpenAI-compatible API base URL
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        # Build messages with the system instructions
        messages = [
            {"role": "system", "content": SYSTEM_INSTRUCTION}
        ]
        
        # Format and append conversation history
        for msg in payload.history:
            role = "assistant" if msg.role in ["assistant", "bot", "model"] else "user"
            messages.append({"role": role, "content": msg.content})
            
        # Append the new user message
        messages.append({"role": "user", "content": payload.message})
        
        # Call Groq Chat Completions endpoint with llama-3.3-70b-versatile and scrape_my_profiles tool
        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=messages,
            tools=[SCRAPE_TOOL_SCHEMA],
            tool_choice="auto",
            temperature=0.7,
            max_tokens=1000,
        )
        
        response_message = response.choices[0].message
        
        # Check if model requested a tool call
        if response_message.tool_calls:
            # Append assistant message with tool calls
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                if function_name == "scrape_my_profiles":
                    try:
                        args = json.loads(tool_call.function.arguments)
                        platform_arg = args.get("platform", "github")
                    except Exception:
                        platform_arg = "github"
                        
                    tool_output = scrape_my_profiles.invoke({"platform": platform_arg})
                    
                    # Append tool result message
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(tool_output),
                    })
            
            # Send second request with tool outputs included
            second_response = client.chat.completions.create(
                model='llama-3.3-70b-versatile',
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
            )
            return ChatResponse(response=second_response.choices[0].message.content or "No response content.")

        return ChatResponse(response=response_message.content or "No response content.")

        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating chat response: {str(e)}"
        )

# Mount the static portfolio files (index.html, script.js, styles.css) at root '/'
portfolio_dir = Path(__file__).resolve().parent.parent
app.mount("/", StaticFiles(directory=str(portfolio_dir), html=True), name="static")

