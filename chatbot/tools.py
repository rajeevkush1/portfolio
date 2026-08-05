import os
from typing import Optional
from dotenv import load_dotenv
from langchain_core.tools import tool

# Attempt importing FirecrawlApp or Firecrawl from the firecrawl SDK
try:
    from firecrawl import FirecrawlApp
except ImportError:
    try:
        from firecrawl import Firecrawl as FirecrawlApp
    except ImportError:
        FirecrawlApp = None

from pathlib import Path

# Load environment variables from chatbot/.env and root .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)
load_dotenv()


# Dictionary of allowed profile URLs for Rajeev Kushwaha
ALLOWED_PROFILES = {
    "linkedin": "https://www.linkedin.com/in/rajeev-kushwaha-578b4b242/",
    "github": "https://github.com/rajeevkush1",
    "kaggle": "https://www.kaggle.com/rajeevkushwaha"
}


@tool
def scrape_my_profiles(platform: str, api_key: Optional[str] = None) -> str:
    """
    Scrapes the user's personal profiles to retrieve up-to-date information.
    
    Args:
        platform (str): The platform profile to scrape. Must be 'github', 'linkedin', or 'kaggle'.
        api_key (Optional[str]): Optional Firecrawl API key. If not provided, FIRECRAWL_API_KEY from environment variables will be used.
        
    Returns:
        str: Markdown content scraped from the profile page, or an error message.
    """
    platform_key = platform.strip().lower()
    
    # 1. Enforce strict whitelisting so the agent can ONLY hit authorized profiles
    if platform_key not in ALLOWED_PROFILES:
        allowed_list = ", ".join(ALLOWED_PROFILES.keys())
        return f"Error: I am only authorized to scrape the following platforms: {allowed_list}."
        
    target_url = ALLOWED_PROFILES[platform_key]
    
    # 2. Check if Firecrawl SDK is installed
    if FirecrawlApp is None:
        return "Error: `firecrawl-py` library is not installed. Please install it via `pip install firecrawl-py` or `uv add firecrawl-py`."
        
    # 3. Retrieve API key
    effective_api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
    if not effective_api_key:
        return "Error: FIRECRAWL_API_KEY is not configured. Please set it in environment variables or pass it to the tool."
        
    # 4. Execute the scrape using Firecrawl
    try:
        scraper = FirecrawlApp(api_key=effective_api_key)
        
        # Support Firecrawl v2 and v1 methods
        if hasattr(scraper, 'scrape'):
            result = scraper.scrape(target_url, formats=['markdown'])
        elif hasattr(scraper, 'scrape_url'):
            result = scraper.scrape_url(target_url, params={'formats': ['markdown']})
        else:
            return "Error: Unrecognized Firecrawl SDK interface."
            
        # Extract markdown content from Document object or dictionary
        if hasattr(result, 'markdown') and result.markdown:
            return result.markdown
        elif isinstance(result, dict):
            return result.get("markdown") or result.get("content") or str(result)
        return str(result)
    except Exception as e:
        return f"Failed to scrape {platform_key} profile ({target_url}): {str(e)}"

