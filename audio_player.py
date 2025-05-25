# Using pygame because its so cool
import pygame
import time
import os
import soundfile

class AudioPlayer:
    def __init__(self):
        # Setup pymixer with frequency and buffer that will stop stuttering audio
        pygame.mixer.init(frequency=48000, buffer=1024)



    def play_audio(self, audio_path, sleep_while_playing=True, delete_file=False):
        # if not already initialized, reinitialize
        if(not pygame.mixer.get_init()):
            pygame.mixer.init(frequency=48000, buffer=1024)
        
        # play audio
        audio = pygame.mixer.Sound(audio_path).play()

        # stop running script while playing to allow character to finish
        if(sleep_while_playing):
            # elevenlabs returns wav, calculate filesize to determine sleeptime
            wav_obj = soundfile.SoundFile(audio_path)
            sleep_time = wav_obj.frames / wav_obj.samplerate # total frames / fps
            wav_obj.close()

            time.sleep(sleep_time)

            if(delete_file):
                # delete file ONLY after it finishes
                # stop pySound before deleting the file
                audio.stop()
                pygame.mixer.quit()

                os.remove(audio_path)
                print("Audio file removed successfully.")

# Quick debugging test
if __name__ == "__main__":
    audio_player = AudioPlayer()
    pth = r"" # path goes here
    audio_player.play_audio(pth, True, True)






