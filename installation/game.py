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

# imports Catastrophe class
from catastrophe import Catastrophe

# Loads in .env file which needs to be located in the same folder as this file
load_dotenv()
# Fetches api key from .env file (can be generated at https://platform.openai.com/account/api-keys)
openai.api_key = os.getenv("OPENAI_API_KEY")

# client für export zu touchdesigner
client = udp_client.SimpleUDPClient("127.0.0.1", 7000)

# Copied from: https://www.w3resource.com/python-exercises/python-basic-exercise-55.php
# Gets current ip address of pc
ip_address = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                           if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)),
                                                                 s.getsockname()[0], s.close()) for s in
                                                                [socket.socket(socket.AF_INET,
                                                                               socket.SOCK_DGRAM)]][0][1]]) if l][0][0]


class Symptoms:
    def __init__(self):
        # Start values
        self.prompt = "Generiere 25 kurze, fiktive & sarkastische Schlagzeilen über den Klimawandel. Die Schlagzeilen sollen keine Jahreszahlen oder den Begriff Klimawandel beinhalten. Geb die Schlagzeilen als Liste mit dem key 'headlines' in einer JSON zurück"
        self.is_game_running = False
        self.start_year = 2025
        self.year = self.start_year
        self.count = 0
        self.death_count = 0
        self.temperature = 1
        self.free_regions = ["na1", "na2", "eu1", "sa1", "sa2", "af1", "af2", "af3", "as1", "as2", "as3", "oc1"]
        self.occupied_regions = set()
        self.region_data = {
            "na1": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,  # Muss in Prozent übergeben werden
            },
            "na2": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,  # Muss in Prozent übergeben werden
            },
            "eu1": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,  # Muss in Prozent übergeben werden
            },
            "sa1": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,  # Muss in Prozent übergeben werden
            },
            "sa2": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,  # Muss in Prozent übergeben werden
            },
            "af1": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,  # Muss in Prozent übergeben werden
            },
            "af2": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,  # Muss in Prozent übergeben werden
            },
            "af3": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,  # Muss in Prozent übergeben werden
            },
            "as1": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,  # Muss in Prozent übergeben werden
            },
            "as2": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,  # Muss in Prozent übergeben werden
            },
            "as3": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,  # Muss in Prozent übergeben werden
            },
            "oc1": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,  # Muss in Prozent übergeben werden
            },
        }
        self.headlines = []
        self.sensor_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.is_test_event_active = False

    def get_inputs(self):
        # Writes sensor input from Pi Cap into variable
        def get_diff_values(unused_addr, *args):
            self.sensor_values = args

        # Maps dispatcher to path of diff values
        dispatcher = Dispatcher()
        dispatcher.map("/diff*", get_diff_values)

        # Initiates OSC server
        server = osc_server.BlockingOSCUDPServer((ip_address, 3000), dispatcher)
        server.serve_forever()

    def generate_headlines(self, verbose):
        while True:
            if len(self.headlines) < 100:
                if verbose:
                    print("Filling up headlines... (currently " + str(len(self.headlines)) + "/100)")
                # Calls GPT API and requests headlines
                gpt_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user",
                         "content": self.prompt}
                    ]
                )
                try:
                    # Converts response into JSON
                    headlines_json = json.loads(gpt_response.choices[0].message.content)
                    # Adds new headlines to headlines array
                    for headline in headlines_json['headlines']:
                        self.headlines.append(headline)
                    # Rests for 5 seconds
                    time.sleep(5)
                except Exception:
                    # Catches wrong response from GPT API
                    print('GPT returned wrong data format')

    def get_temperature(self):
        # Temperature graph
        self.temperature = 1.5 * math.cos(0.04 * (self.year - self.start_year) + math.pi) + 2.5
        print(self.temperature)
        # Sendet Temperatur an Textfile
        speichern_news("/temperature/", self.temperature)

    def trigger_headline(self):
        if len(self.headlines) > 0:
            # Randomly picks headline from array
            index = random.randrange(0, len(self.headlines))
            print(self.headlines[index])
            # Sendet Headline an Textfile
            speichern_news("/headline/", self.headlines[index])
            # Removes chosen headline from array
            del self.headlines[index]
        else:
            print("--- Blank (headline) ---")
            # Später löschen
            speichern_news("/headline/", "nix")

    def trigger_catastrophe(self):
        # TODO: Melli News input
        if len(self.free_regions) != 0:
            selected_region = random.choice(self.free_regions)
            self.occupied_regions.add(selected_region)
            self.free_regions.remove(selected_region)
            catastrophe = Catastrophe(selected_region, self.temperature)
            print(catastrophe.type + " in region " + selected_region + " is active " + "(" + str(
                catastrophe.electrode_index) + ")\n")
            self.region_data[selected_region]["is_active"] = True
            self.region_data[selected_region]["type"] = catastrophe.type
            self.region_data[selected_region]["resolution_percentage"] = 0
            current_windup = 0
            current_duration = 0
            current_resolution_time = 0
            while current_windup < catastrophe.wind_up and self.is_game_running is True:
                if self.sensor_values[catastrophe.electrode_index] > 100:
                    current_resolution_time += 0.01
                    self.region_data[selected_region][
                        "resolution_percentage"] = current_resolution_time / catastrophe.resolution_time
                if current_resolution_time >= catastrophe.resolution_time:
                    break
                current_windup += 0.01
                time.sleep(0.01)
            if catastrophe.resolution_time >= current_resolution_time:
                while current_duration < catastrophe.duration and self.is_game_running is True:
                    if self.sensor_values[catastrophe.electrode_index] > 100:
                        current_resolution_time += 0.01
                        self.region_data[selected_region][
                            "resolution_percentage"] = current_resolution_time / catastrophe.resolution_time
                    if current_resolution_time >= catastrophe.resolution_time:
                        break
                    self.death_count += catastrophe.deaths_per_second * 0.01
                    current_duration += 0.01
                    time.sleep(0.01)
            self.region_data[selected_region]["is_active"] = False
            print(catastrophe.type + " in region " + selected_region + " is resolved " + "(" + str(
                catastrophe.electrode_index) + ")\n")
            time.sleep(2)
            self.free_regions.append(selected_region)
            self.occupied_regions.remove(selected_region)
        else:
            print("--- Blank (catastrophe) ---")
            speichern_news("/catastrophe/", "nix")

    def trigger_event(self):
        # Chance of headline occurring
        chance_headline = 0.25
        # Base chance of catastrophe occurring
        base_chance_catastrophe = 0.10
        # Temperature increase since game start
        temperature_delta = self.temperature - 1
        # Chance of nothing happening
        chance_remaining = 1 - chance_headline - base_chance_catastrophe
        # Chance of catastrophe occurring depending on temperature
        chance_catastrophe = base_chance_catastrophe + (
                math.cos(math.pi + (temperature_delta / 3) * math.pi) + 1) * chance_remaining

        # Picks random number
        random_number = random.randrange(0, 101) / 100

        # Triggers headline
        if random_number < chance_headline:
            self.trigger_headline()
        # Triggers catastrophe
        elif random_number < (chance_headline + chance_catastrophe):
            Thread(target=self.trigger_catastrophe).start()

        # Triggers nothing
        else:
            print("--- Blank ---")
            # Später löschen
            speichern_news("/catastrophe/", "nix")

    def run(self, skip_headlines):
        while True:
            print("Touch any electrode to start game.")
            while self.is_game_running is False:
                for sensor in self.sensor_values:
                    if sensor > 100:
                        self.__init__()
                        self.is_game_running = True
                        break

            # Waits for headline generation until at least 20 are available
            if len(self.headlines) < 20 and not skip_headlines:
                print("Waiting for headlines...")
            while len(self.headlines) < 20 and not skip_headlines:
                pass

            # Main game loop
            while self.year < 2100:
                self.trigger_event()
                print(str(int(self.death_count)) + " people have died.")
                self.count += 1
                if self.count == 5:
                    self.year += 1
                    print(self.year)
                    speichern_news("/year/", self.year)
                    self.count = 0
                    self.get_temperature()
                time.sleep(1)
            self.is_game_running = False

    def main(self, skip_headlines=True, verbose=True):
        # headline generation thread
        if not skip_headlines:
            Thread(target=self.generate_headlines, args=(verbose,)).start()

        # runtime thread
        Thread(target=self.run, args=(skip_headlines,)).start()

        # input fetching thread
        Thread(target=self.get_inputs(), daemon=True).start()


# Speichert alle News für die GUI in news.txt
def speichern_news(type, value):
    with open("news.txt", 'a') as datei:
        datei.write(type + str(value) + '\n')


symptoms = Symptoms()

# Props:
# skip_headlines: Whether headline generation is skipped (defaults to False)
# verbose: Prints progress of headline generation (defaults to True)
symptoms.main(skip_headlines=False, verbose=True)
