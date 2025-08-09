from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import pyttsx3
import speech_recognition as sr
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat(message: Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant named Jarvis."},
                {"role": "user", "content": message.text}
            ]
        )
        ai_text = response.choices[0].message["content"]

        # Text-to-speech
        engine = pyttsx3.init()
        engine.say(ai_text)
        engine.runAndWait()

        return {"reply": ai_text}
    except Exception as e:
        return {"error": str(e)}

@app.get("/listen")
async def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return {"heard": text}
    except sr.UnknownValueError:
        return {"error": "Sorry, I could not understand the audio."}
    except sr.RequestError as e:
        return {"error": f"Speech recognition service error: {str(e)}"}
