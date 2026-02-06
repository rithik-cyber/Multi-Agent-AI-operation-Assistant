import os
from dotenv import load_dotenv
from groq import Groq
from llm.logger import logger

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing in .env")

client = Groq(api_key=GROQ_API_KEY)

logger.info("Groq client initialized successfully")

