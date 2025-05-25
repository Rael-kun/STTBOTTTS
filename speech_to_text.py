import time
import azure.cognitiveservices.speech as speechsdk
import keyboard
import os
from dotenv import load_dotenv

load_dotenv()

# API Key here
speech_key= os.getenv("TTS_KEY")
service_region = "centralus"

class STT_Manager():
    speechConfig = None
    speechRecognize = None

    def __init__(self):
        self.start_btn = "q"
        self.finish_button = "p"
        # You need both the api key and the service region, return an error otherwise
        try:
            self.speechConfig = speechsdk.SpeechConfig(subscription = speech_key, region = service_region)
        except TypeError:
            exit("You forgot either the API key or the service region.")
        
        self.speechConfig.speech_recognition_language = "en-US"
        self.speechConfig.set_profanity(speechsdk.ProfanityOption.Raw)

    def speech_from_microphone(self):
        finished = False
        # Create recognizer, prints out heard input continuously
        self.speechRecognize = speechsdk.SpeechRecognizer(speech_config = self.speechConfig)

        def current_recog(event_arg: speechsdk.SpeechRecognitionEventArgs):
            print("Recognized: {}".format(event_arg))

        self.speechRecognize.recognized.connect(current_recog)

        # If quitting out:
        def end_stt(event_arg: speechsdk.SessionEventArgs):
            print("Speech-to-text ending due to {}.".format(event_arg))
            # Weird func to change finished, otherwise it doesn't update in the global scope
            nonlocal finished
            finished = True

        self.speechRecognize.session_stopped.connect(end_stt)
        self.speechRecognize.canceled.connect(end_stt)

        # Give the recognizer the total current text
        total_cur_text = []

        def read_total_text(event_arg):
            total_cur_text.append(event_arg.result.text)

        self.speechRecognize.recognized.connect(read_total_text)

        # With all that set up, we can now begin the speech-to-text process
        speech_to_text = self.speechRecognize.start_continuous_recognition_async()
        speech_to_text.get()
        print("Voice recognition has begun, speak into the mic.")

        # break out of speech recognition if the user hits the end key
        while(finished != True):
            if(keyboard.read_key() == self.finish_button):
                print("Voice recognition ended by user.")
                self.speechRecognize.stop_continuous_recognition_async()
                break

        # Completed, display results back to user
        finished_result = " ".join(total_cur_text).strip()
        print(f"\n\n Text Gathered: \n\n{finished_result} \n\n")
        
        return finished_result
    

# Quick debugging test
if __name__ == "__main__":
    manager = STT_Manager()

    while(True):
        result = manager.speech_from_microphone()
        print("Result: ", result)
        time.sleep(60)



            







