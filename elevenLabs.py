from elevenlabs import stream, voices, play, save
from elevenlabs.client import ElevenLabs
import time
import os
from dotenv import load_dotenv

load_dotenv()
# API Key here
elevenLabs_key = os.getenv("11LABS_KEY")

class ElevenLabsManager:
    def __init__(self):
        try:
            self.filenum = 0
            self.client = ElevenLabs(api_key=elevenLabs_key)
        except TypeError:
            print("Error, you probably forgot the API key.")
    
    def tts_to_play(self, input_text, voice=""):
        if(not voice):
            print("Forgot to use voice!")
            return
        
        audio = self.client.generate(
            text = input_text,
            voice = voice,
            model= "eleven_multilingual_v2"
        )
        play(audio)
    
    def tts_to_file(self, input_text, voice="", subdirectory=""):
        if(not voice):
            print("Forgot to use voice!")
            return
        
        audio_file = self.client.generate(
            text = input_text,
            voice = voice,
            model= "eleven_multilingual_v2"
        )
        # create unique filename
        file_name = f"__Msg[{self.filenum}]{str(hash(input_text))}.wav"
        self.filenum += 1
        tts_file = os.path.join(os.path.abspath(os.curdir), subdirectory, file_name)
        save(audio_file, tts_file)
        return tts_file

if __name__ == "__main__":
    elevenlabs_manager = ElevenLabsManager()

    elevenlabs_manager.tts_to_play("Where did everyone go?", "Tingyun")
    #test = elevenlabs_manager.tts_to_file("Where am I?", "Tingyun")
    #print(test)
    print("Finished with all tests.")
