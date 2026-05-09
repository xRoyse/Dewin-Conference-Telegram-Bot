import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "7839084541:AAERFX89zJlduW59IdJjUduUpstZxx4RDCs")
JWT_SECRET = os.getenv("JWT_SECRET", "dewin_bot_secret")
JWT_ALGORITHM = "HS256"

