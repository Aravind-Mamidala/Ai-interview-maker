from gtts import gTTS
import tempfile

def speak_question(text):
    tts = gTTS(text=text, lang='en')

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        return tmp.name