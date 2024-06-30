import os
from dotenv import load_dotenv

load_dotenv()

ATHINA_API_BASE_URL = os.getenv("ATHINA_API_BASE_URL", "https://log.athina.ai")
