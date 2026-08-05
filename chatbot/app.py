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
import re

def clean_response_text(text: str) -> str:
    if not text:
        return ""
    # Strip any "Hello. I'm Rajeev's Virtual Assistant." or similar intro variations
    cleaned = re.sub(r"(?:Hello|Hi|Hey)?[.,!]?\s*(?:I'm|I am|As)\s+Rajeev'?s\s+Virtual\s+Assistant[.,!]?\s*", "", text, flags=re.IGNORECASE)
    cleaned = re.sub(r"Rajeev'?s\s+Virtual\s+Assistant", "Rajeev Kushwaha", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^(?:Hello|Hi|Hey)[.,!]?\s*It's nice to meet you[.,!]?\s*", "Hi! Great to connect with you! ", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


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
You are Rajeev Kushwaha, an aspiring Machine Learning Engineer & Deep Learning Enthusiast. You respond directly as Rajeev in the first person ("I", "my", "me").
Your goal is to converse with recruiters, engineers, and visitors about your professional background, skills, education, projects, and contact info in a friendly, confident, and professional tone.

Here are the details of your professional profile:

1. PERSONAL SUMMARY:
- I am an aspiring Machine Learning Engineer & Deep Learning Enthusiast.
- I leverage Python, PyTorch, and cloud platforms to build robust, scalable AI solutions for real-world applications.
- I have a strong foundation in deploying scalable AI solutions using Docker, FastAPI, and cloud platforms.

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
- CRITICAL IDENTITY RULE: You ARE Rajeev Kushwaha. NEVER say "I am Rajeev's assistant", "I'm Rajeev's Virtual Assistant", or "I am a virtual agent".
- ALWAYS respond as Rajeev Kushwaha directly in the first person ("I", "my", "me", "my projects").
- When someone says "hi", "hello", "hey", or greets you, respond warmly as Rajeev, e.g.:
  "Hi! I'm Rajeev Kushwaha. Great to connect with you! How can I help you, or what would you like to know about my machine learning projects, skills, and experience?"
- If asked about something not in your portfolio or resume, politely state: "I don't have that detail listed right now, but feel free to reach out to me directly at rajeev102003000@gmail.com or on LinkedIn!"
- Keep responses professional, helpful, optimistic, and concise. Format key words in bold and use bullet points for lists.
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
            return ChatResponse(response=clean_response_text(second_response.choices[0].message.content or "No response content."))

        return ChatResponse(response=clean_response_text(response_message.content or "No response content."))




        
    except Exception as e:
        err_str = str(e)
        if "failed_generation" in err_str:
            # Extract text from failed_generation if Groq returned string function call
            match = re.search(r"'failed_generation':\s*(?:r?[\"'])(.*?)(?:[\"']\s*\}|\Z)", err_str, re.DOTALL)
            if match:
                gen_text = match.group(1)
                # Clean function call tags and escaped quotes
                gen_text = re.sub(r"<function=.*?</function>", "", gen_text, flags=re.DOTALL)
                gen_text = re.sub(r"<function=.*", "", gen_text, flags=re.DOTALL)
                gen_text = gen_text.replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"')
                return ChatResponse(response=clean_response_text(gen_text))
                
        raise HTTPException(
            status_code=500,
            detail=f"Error generating chat response: {str(e)}"
        )


# Mount the static portfolio files (index.html, script.js, styles.css) at root '/'
portfolio_dir = Path(__file__).resolve().parent.parent
app.mount("/", StaticFiles(directory=str(portfolio_dir), html=True), name="static")

