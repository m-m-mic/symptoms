import math
import time
import random
import openai
import json
import os
from dotenv import load_dotenv
from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher
from threading import Thread
import socket

# loads in .env file which needs to be located in the same folder
load_dotenv()
# fetches api key from .env file (can be generated at https://platform.openai.com/account/api-keys)
openai.api_key = os.getenv("OPENAI_API_KEY")

# client für export zu touchdesigner
client = udp_client.SimpleUDPClient("127.0.0.1", 7000)

# copied from: https://www.w3resource.com/python-exercises/python-basic-exercise-55.php
# gets current ip address of pc
ip_address = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, 
socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

class Catastrophe:
    def __init__(self):
        self.type = 'hurricane'
        self.duration = 100
        self.wind_up = 10
        self.deaths_per_second = 10

class Symptoms:
    def __init__(self):
        # Start values
        self.prompt = "Generiere 25 kurze, fiktive & sarkastische Schlagzeilen über den Klimawandel. Die Schlagzeilen sollen keine Jahreszahlen oder den Begriff Klimawandel beinhalten. Geb die Schlagzeilen als Liste mit dem key 'headlines' in einer JSON zurück"
        self.did_game_end = False
        self.start_year = 2025
        self.year = self.start_year
        self.count = 1
        self.death_count = 0
        self.temperature = 1
        self.free_regions = ("na1", "na2", "eu1", "eu2", "sa1", "sa2", "me1", "af1", "af2", "as1", "as2", "oc1")
        self.occupied_regions = set()
        self.region_data = {
            "na1": {
                "is_active": False,
                "type": None,
                "duration": None,
                "wind_up": None,
                "deaths_per_second": None,
                "resolution_time": None,
            },
        }
        self.headlines = []
        self.sensor_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.is_test_event_active = False

    def get_inputs(self):
        # Writes sensor input from Pi Cap into variable
        def get_diff_values(unused_addr, *args):
            self.sensor_values = args
            # print(self.sensor_values)

        # Maps dispatcher to path of diff values
        dispatcher = Dispatcher()
        dispatcher.map("/diff*", get_diff_values)

        # Initiates OSC server
        server = osc_server.BlockingOSCUDPServer((ip_address, 3000), dispatcher)
        server.serve_forever()

    def generate_headlines(self):
        # TODO: needs to run alongside runtime method to reduce wait times
        while len(self.headlines) < 100:
            print("Generating headlines... (" + str(len(self.headlines)) + "/100)")
            gpt_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user",
                     "content": self.prompt}
                ]
            )
            try:
                headlines_json = json.loads(gpt_response.choices[0].message.content)
                for headline in headlines_json['headlines']:
                    self.headlines.append(headline)
            except Exception:
                # Catches wrong response from GPT API
                print('GPT returned wrong data format')

    def get_temperature(self):
        self.temperature = 1.5 * math.cos(0.04 * (self.year - self.start_year) + math.pi) + 2.5
        print(self.temperature)
        # Sendet Temperatur an TouchDesigner
        client.send_message("/temperature", self.temperature)

    def trigger_headline(self):
        if len(self.headlines) > 0:
            index = random.randrange(0, len(self.headlines))
            print(self.headlines[index])
            # Sendet Headline an TouchDesigner
            client.send_message("/headline", self.headlines[index])
            del self.headlines[index]
        else:
            print("Ran out of headlines :((((")
            client.send_message("/headline", "Ran out of headlines :((((")

    def trigger_catastrophe(self):
        self.is_test_event_active = True
        catastrophes = ['drought', 'hurricane', 'flood', 'wildfire', 'sandstorm']
        catastrophe = random.choice(catastrophes)
        print(f'Oh no! A {catastrophe}  ＼(º □ º l|l)/')
        # Sendet Katastrophe an TouchDesigner
        client.send_message("/catastrophe", catastrophe)
        while self.sensor_values[0] < 100:
            time.sleep(0.01)
        print(f'{catastrophe} resolved.')
        self.is_test_event_active = False
        time.sleep(0.5)

    def trigger_event(self):
        chance_headline = 0.25
        base_chance_catastrophe = 0.10
        temperature_delta = self.temperature - 1
        chance_remaining = 1 - chance_headline - base_chance_catastrophe
        chance_catastrophe = base_chance_catastrophe + (
                math.cos(math.pi + (temperature_delta / 3) * math.pi) + 1) * chance_remaining
        random_number = random.randrange(0, 101) / 100

        if random_number < chance_headline:
            self.trigger_headline()
        elif random_number < (chance_headline + chance_catastrophe):
            self.trigger_catastrophe()

    def run(self, skip_headlines):
        self.did_game_end = False
        if len(self.headlines) == 0 and not skip_headlines:
            self.generate_headlines()
        while self.year < 2100:
            # self.trigger_event()
            if not self.is_test_event_active:
                Thread(target=self.trigger_catastrophe).start()
            self.count += 1
            if self.count == 6:
                self.year += 1
                print(self.year)
                # Sendet Jahreszahl an TouchDesigner
                client.send_message("/year", self.year)
                self.count = 1
                self.get_temperature()
            time.sleep(1)
        self.did_game_end = True
        if not skip_headlines:
            self.generate_headlines()

    def main(self, skip_headlines=False):
        # runtime thread
        Thread(target=self.run, args=(skip_headlines,)).start()
        # Thread(target=self.trigger_catastrophe).start()
        # input fetching thread
        Thread(target=self.get_inputs(), daemon=True).start()


symptoms = Symptoms()
symptoms.main(True)
