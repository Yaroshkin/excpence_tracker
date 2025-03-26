import os 
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
API_URL = "http://127.0.0.1:8000/expenses"
REPORT_API_URL = "http://127.0.0.1:8000/report"
REPORT_ALL_URL = "http://127.0.0.1:8000/full_report"