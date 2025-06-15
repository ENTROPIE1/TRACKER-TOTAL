from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env if present
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DB_PATH = os.getenv('DB_PATH', 'tracker.db')

# Ensure database path is absolute
DB_PATH = str(Path(DB_PATH))
