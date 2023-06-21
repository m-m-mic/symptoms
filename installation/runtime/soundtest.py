import playsound
import time

def play_sound():
    while True:
        playsound.playsound("audio/alert.wav")
        time.sleep(2)
        time.sleep(2)


play_sound()
