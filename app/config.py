import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
REDIS_URL = os.getenv('REDIS_URL')
JWT_TOKEN = os.getenv('JWT_TOKEN')
SENTRY_DSN = os.getenv('SENTRY_DSN')
DATABASE_DSN = os.getenv('DATABASE_DSN')
DEVELOPER_ID = os.getenv('DEVELOPER_ID')
