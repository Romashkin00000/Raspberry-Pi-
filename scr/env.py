import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Переменные окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
VOLUME_THRESHOLD = float(os.getenv("VOLUME_THRESHOLD", 0.1))  # Значение по умолчанию 0.1
VIDEO_OUTPUT_PATH = os.getenv("VIDEO_OUTPUT_PATH", "output.mp4")
AUDIO_OUTPUT_PATH = os.getenv("AUDIO_OUTPUT_PATH", "output.wav")