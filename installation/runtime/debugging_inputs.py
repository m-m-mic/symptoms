from pythonosc.udp_client import SimpleUDPClient
from dotenv import load_dotenv
import os
from threading import Thread
import keyboard

load_dotenv()
# gets current ip address of pc
ip_address = os.getenv("IP_ADDRESS")

# osc client port destination
port = 3000


class Debugging:
    def __init__(self):
        # inputs imitating the pi caps output
        self.inputs = [0] * 12
        # key mapping for the debug application
        self.key_mapping = ["a", "s", "d", "f", "g", "h", "j", "k", "l", "ö", "ä", "#"]

    def start_client(self):
        # starts client connection
        client = SimpleUDPClient(ip_address, port)
        print(f'Started client on {ip_address}, port {port}')
        while True:
            client.send_message("/diff", self.inputs)
            # print(self.inputs)

    def get_inputs(self):
        while True:
            # changes values of self.inputs based on keyboard presses (see self.key_mapping)
            for i in range(len(self.inputs)):
                if keyboard.is_pressed(self.key_mapping[i]):
                    # sets value of electrode to 350 if true (which is interpreted as pressed by game.py)
                    self.inputs[i] = 350
                else:
                    self.inputs[i] = 0

    def main(self):
        Thread(target=self.get_inputs, daemon=True).start()
        self.start_client()


debug = Debugging()
debug.main()
