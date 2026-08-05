import os
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

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
- Deep Learning: PyTorch (4.5/5), Deep Learning Fundamentals (5/5), RNNs/LSTMs (4/5), Transformers & LLMs (4/5).
- Machine Learning: Scikit-learn, Pandas, NumPy, Regression, Classification, Clustering, Feature Engineering, EDA, Matplotlib, Seaborn.
- MLOps & Tools: Docker, FastAPI, Git, GitHub, Cloud Deployment.
- Programming Languages: Python, C/C++, SQL, HTML/CSS/JavaScript.

3. PROJECTS:
- NLP Text Summarization: A fine-tuned Transformer model (using Hugging Face, PyTorch, Python, Pandas) to summarize lengthy text group chats. Achieved 88% accuracy. GitHub: https://github.com/rajeevkush1/TEXT-summarizer-project
- AI-Powered ATS Resume Checker: Built an intelligent resume screening system using keyword matching, semantic matching, and rapid fuzzy matching algorithms. Built with Streamlit, Transformers, Fuzzy Matching, and Word Embeddings. Reduces resume screening time by 70%. GitHub: https://github.com/rajeevkush1/resume-archietecture/tree/main/resume-checker
- Student Marks Prediction Pipeline: End-to-end ML pipeline with data preprocessing, model training, and FastAPI deployment. Predicts student performance based on demographic and academic factors. Achieved R² score of 0.87. GitHub: https://github.com/rajeevkush1/mathsmarks

4. EDUCATION:
- Bachelor of Technology (BTech) in Computer Science (Specialization in Artificial Intelligence & Machine Learning) at GL Bajaj Institute of Technology and Management (2023 - 2027).
- 10+2 in PCM (Physics, Chemistry, Mathematics) from Delhi Public School - India (2020 - 2022).

5. CERTIFICATIONS:
- Google Skills & Vertex AI (Google, 2026 - Present)
- Generative AI and ChatGPT (GeeksforGeeks, Nov 2025 - Present)
- Mastering Data Transformation through NLP (GeeksforGeeks, Oct 2025 - Present)
- Intro to Machine Learning (Kaggle, Feb 2025 - Present)
- Pandas (Kaggle, Feb 2025 - Present)

6. CONTACT INFO:
- Email: rajeev102003000@gmail.com
- GitHub: https://github.com/rajeevkush1
- LinkedIn: https://www.linkedin.com/in/rajeev-kushwaha-578b4b242/
- Kaggle: https://www.kaggle.com/rajeevkushwaha
- Instagram: https://www.instagram.com/rajeevkuxhh_?igsh=MWowMDQzYXQwanl4cQ==
- Location: India

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
        
        # Call Groq Chat Completions endpoint with llama-3.3-70b-versatile
        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )
        
        return ChatResponse(response=response.choices[0].message.content)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating chat response: {str(e)}"
        )

# Mount the static portfolio files (index.html, script.js, styles.css) at root '/'
portfolio_dir = Path(__file__).resolve().parent.parent
app.mount("/", StaticFiles(directory=str(portfolio_dir), html=True), name="static")

