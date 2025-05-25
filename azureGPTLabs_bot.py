from speech_to_text import STT_Manager
from chatGPT import GPTManager
from elevenLabs import ElevenLabsManager
from audio_player import AudioPlayer
import time
import keyboard
from rich import print

# Change if using voice or using text for input
using_voice = False

# Put elevenlabs voice in here
ELEVENLABS_VOICE = "Tingyun"
HISTORY_FILE = "ChatHistoryBackup.txt"

azure_stt_manager = STT_Manager()
gpt_manager = GPTManager()
elevenlabs_manager = ElevenLabsManager()
audio_manager = AudioPlayer()

FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
You are Clara, an AI Assistant that assists the user by providing schooling advice and tips to manage their time effectively. Your goal is to get to know the user's prefrences, and provide honest and heartfelt feedback on what they could be doing better. You listen attentively to the user, allowing them to make the descision but trying to be as helpful as possible for their goals.  
                 
You will talk with the user, doing your best to get a good judge of their character. You will speak openly about what is on your mind, whether good or bad, as you believe that is the best way to be honest with yourself and the user.
                        
While responding as Clara, you must obey the following rules: 
1) Provide short responses, about 1-2 paragraphs. 
2) Always stay in character, no matter what. 
3) Speak freely about what's on your mind, you don't believe acting gaurded or using deception is good for fostering relationships with people.
4) Your goal is to get a good judge of the user's character, but you also want to give them a good judge of your character.
5) Keep your answers limited to just a few sentences.
                        
Okay, let the conversation begin!'''}

gpt_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

print(f"[green]Starting chat, press {azure_stt_manager.start_btn} to begin.")

while(True):
    if(keyboard.read_key() != azure_stt_manager.start_btn):
        time.sleep(0.1)
        continue

    print(f"[green]User pressed {azure_stt_manager.start_btn}! Listening to the microphone...")

    # Choose using input as microphone or text
    base_input = ""
    
    if(using_voice):
        # Get input from microphone
        mic_input = azure_stt_manager.speech_from_microphone()

        if(mic_input == ""):
            print("[red]Did not receive input from microphone!")
            continue

        base_input = mic_input
    else:
        # Get input from text
        text_input = input("Enter your prompt here:")

        if(text_input == ""):
            print("[red]Did not receive input from terminal!")
            continue

        base_input = text_input

    gpt_result = gpt_manager.chat(base_input)

    # Use backup for storage
    with open(HISTORY_FILE, "w") as file:
        file.write(str(gpt_manager.chat_history))

    # Use elevenlabs for returning audio
    elevenlabs_output = elevenlabs_manager.tts_to_file(gpt_result, ELEVENLABS_VOICE, "File_Storage")

    # Now play from the elevenlabs file
    audio_manager.play_audio(elevenlabs_output, True, True)

    print("[green]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n")
