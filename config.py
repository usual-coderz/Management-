# ============================================================
#Group Manager Bot
# Author: LearningBotsOfficial (https://github.com/LearningBotsOfficial) 
# Support: https://t.me/LearningBotsCommunity
# Channel: https://t.me/learning_bots
# YouTube: https://youtube.com/@learning_bots
# License: Open-source (keep credits, no resale)
# ============================================================

import os
from dotenv import load_dotenv

load_dotenv()

# Required configurations
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = os.getenv("DB_NAME", "Cluster0")

OWNER_ID = int(os.getenv("OWNER_ID", 0))
BOT_USERNAME = os.getenv("BOT_USERNAME", "")

SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "")
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "")
START_IMAGE = os.getenv("START_IMAGE", "")

LOGS_GC = -1003690935546