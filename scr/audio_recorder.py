import pyaudio
import wave
from collections import deque


class AudioRecorder:
    def __init__(self, buffer_seconds, rate=44100, channels=1):
        self.rate = rate
        self.channels = channels
        self.buffer = deque(maxlen=buffer_seconds * rate)

    def record(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=self.channels, rate=self.rate, input=True,
                        frames_per_buffer=1024)

        while True:
            data = stream.read(1024, exception_on_overflow=False)
            self.buffer.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def save_audio(self):
        audio_file = "audio.wav"
        with wave.open(audio_file, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.rate)
            wf.writeframes(b"".join(self.buffer))

        return audio_file