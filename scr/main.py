import os
import time
import dotenv
from threading import Thread, Event
from video_recorder import VideoRecorder
from audio_recorder import AudioRecorder
from plate_detector import PlateDetector
from telegram_sender import TelegramSender
from env import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, VOLUME_THRESHOLD

print(f"Громкость порога: {VOLUME_THRESHOLD}")
dotenv.load_dotenv("../config/.env")

BUFFER_SECONDS = 40  # Сколько секунд видео/аудио храним перед сохранением
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 20

record_event = Event()

video_recorder = VideoRecorder(FRAME_WIDTH, FRAME_HEIGHT, FPS, BUFFER_SECONDS)
audio_recorder = AudioRecorder(BUFFER_SECONDS)
plate_detector = PlateDetector("models/haarcascade_russian_plate_number.xml")
telegram_sender = TelegramSender(os.getenv(TELEGRAM_BOT_TOKEN), os.getenv(TELEGRAM_CHAT_ID))

def start_monitoring():
    audio_thread = Thread(target=audio_recorder.record)
    audio_thread.start()

    while True:
        frame = video_recorder.capture_frame()
        if plate_detector.detect(frame):
            print("🚗 Обнаружен номер! Сохраняем видео...")
            save_and_send()
            break

    record_event.set()
    audio_thread.join()

def save_and_send():
    video_path, audio_path, output_path = video_recorder.save_video(), audio_recorder.save_audio(), "output.mp4"

    # Объединяем видео и аудио через ffmpeg
    os.system(f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac {output_path} -y")

    telegram_sender.send_video(output_path)

if __name__ == "__main__":
    start_monitoring()