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
from get_ip import get_ip

# UPD Client for world map visualisation
client = udp_client.SimpleUDPClient("127.0.0.1", 12000)

# imports Catastrophe class
from catastrophe import Catastrophe

# gets headline constructors
from construct_headline import construct_start_headline, construct_end_headline, get_source

# Loads in .env file which needs to be located in the same folder as this file
load_dotenv()
# Fetches api key from .env file (can be generated at https://platform.openai.com/account/api-keys)
openai.api_key = os.getenv("OPENAI_API_KEY")



# Gets current ip address of pc
ip_address = get_ip()

key_mapping = ["a", "s", "d", "f", "g", "h", "j", "k", "l", "ö", "ä", "#"]


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
                "resolution_percentage": 0,
            },
            "na2": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,
            },
            "eu1": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,
            },
            "sa1": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,
            },
            "sa2": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,
            },
            "af1": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,
            },
            "af2": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,
            },
            "af3": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,
            },
            "as1": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,
            },
            "as2": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,
            },
            "as3": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,
            },
            "oc1": {
                "is_active": False,
                "type": None,
                "resolution_percentage": 0,
            },
        }
        self.headlines = []
        self.sensor_values = [0] * 12

    def reset_attributes(self):
        generated_headlines = self.headlines
        self.__init__()
        self.headlines = generated_headlines

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
                try:
                    # Calls GPT API and requests headlines
                    gpt_response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "user",
                             "content": self.prompt}
                        ]
                    )
                    # Converts response into JSON
                    headlines_json = json.loads(gpt_response.choices[0].message.content)
                    # Adds new headlines to headlines array
                    for headline in headlines_json['headlines']:
                        self.headlines.append({"headline": headline, "source": get_source()})
                    # Rests for 5 seconds
                    time.sleep(5)
                except Exception as e:
                    # Catches bad response from GPT API
                    print("Error while generating headlines:", e)

    def set_temperature(self):
        # Temperature graph
        self.temperature = 1.5 * math.cos(0.04 * (self.year - self.start_year) + math.pi) + 2.5
        # Sendet Temperatur an Textfile
        # speichern_news("/temperature/", self.temperature)

    def trigger_headline(self):
        if len(self.headlines) > 0:
            # Randomly picks headline from array
            index = random.randrange(0, len(self.headlines))
            headline = self.headlines[index]
            print(headline["headline"] + " - " + headline["source"])
            # Sendet Headline an Textfile
            # speichern_news("/headline/", self.headlines[index])
            # Removes chosen headline from array
            del self.headlines[index]
        else:
            print("--- Blank (headline) ---")
            # Später löschen
            # speichern_news("/headline/", "nix")

    def trigger_catastrophe(self):
        # TODO: Melli News input
        if len(self.free_regions) != 0:
            # Moves region from free to occupied
            selected_region = random.choice(self.free_regions)
            self.occupied_regions.add(selected_region)
            self.free_regions.remove(selected_region)

            # Initialises the catastrophe based on selected region and current temperature
            catastrophe = Catastrophe(selected_region, self.temperature)

            # Constructs starting headline based on type and region
            start_headline = {
                "headline": construct_start_headline(selected_region, catastrophe.type),
                "source": get_source()
            }
            print("════════════════════════════════════════════════════════════════════════════════════════════════════════════")
            print(f"!!! CATASTROPHE - {selected_region} - {catastrophe.type} - {catastrophe.wind_up} wind up - {catastrophe.duration} duration - {catastrophe.deaths_per_second} deaths - {catastrophe.resolution_time} resolution time !!!")
            print(start_headline["headline"] + " - " + start_headline["source"])
            print("!!! On electrode " + str(catastrophe.electrode_index) + " - " + key_mapping[
                catastrophe.electrode_index] + " !!!")
            print("════════════════════════════════════════════════════════════════════════════════════════════════════════════")

            # Changes region data
            self.region_data[selected_region]["is_active"] = True
            self.region_data[selected_region]["type"] = catastrophe.type
            self.region_data[selected_region]["resolution_percentage"] = 0

            # Sets starting parameters for catastrophe
            current_windup = 0
            current_duration = 0
            current_resolution_time = 0
            current_death_count = 0
            resolved_by_player = False

            # Wind up period of catastrophe
            while current_windup < catastrophe.wind_up and self.is_game_running is True:
                if self.sensor_values[catastrophe.electrode_index] > 100:
                    current_resolution_time += 0.01
                    self.region_data[selected_region][
                        "resolution_percentage"] = current_resolution_time / catastrophe.resolution_time
                if current_resolution_time >= catastrophe.resolution_time:
                    resolved_by_player = True
                    break
                current_windup += 0.01
                time.sleep(0.01)

            # Main duration of catastrophe if it hasn't been resolved yet
            if catastrophe.resolution_time >= current_resolution_time:
                while current_duration < catastrophe.duration and self.is_game_running is True:
                    if self.sensor_values[catastrophe.electrode_index] > 100:
                        current_resolution_time += 0.01
                        self.region_data[selected_region][
                            "resolution_percentage"] = current_resolution_time / catastrophe.resolution_time
                    if current_resolution_time >= catastrophe.resolution_time:
                        resolved_by_player = True
                        break
                    self.death_count += catastrophe.deaths_per_second * 0.01
                    current_death_count += catastrophe.deaths_per_second * 0.01
                    current_duration += 0.01
                    time.sleep(0.01)

            # Changes region data
            self.region_data[selected_region]["is_active"] = False

            # Constructs ending headline
            end_headline = {
                "headline": construct_end_headline(selected_region, catastrophe.type, current_death_count),
                "source": get_source()
            }
            print("════════════════════════════════════════════════════════════════════════════════════════════════════════════")
            print(f">>> RESOLVED - {selected_region} - {catastrophe.type} - resolved by player? {resolved_by_player} <<<")
            print(end_headline["headline"] + " - " + end_headline["source"])
            print("════════════════════════════════════════════════════════════════════════════════════════════════════════════")

            # Puts region on 2 second cooldown
            time.sleep(2)

            # Moves region back from occupied to free
            self.free_regions.append(selected_region)
            self.occupied_regions.remove(selected_region)
        else:
            print("--- Blank (catastrophe) ---")
            # speichern_news("/catastrophe/", "nix")

    def trigger_event(self):

        client.send_message('/test', str(round(self.death_count)))
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
            # speichern_news("/catastrophe/", "nix")

    def run(self, skip_headlines):
        while True:

            

            # Game starts when any of the sensors are touched by the player
            print("Touch any electrode to start game.\n")
            while self.is_game_running is False:
                if any(sensor > 100 for sensor in self.sensor_values):
                    # Clears all attributes except headlines
                    self.reset_attributes()
                    self.is_game_running = True
                    break

            # Waits for headline generation until at least 20 are available
            if len(self.headlines) < 20 and not skip_headlines:
                print("Waiting for GPT to return headlines...\n")
            while len(self.headlines) < 20 and not skip_headlines:
                pass

            print("/// SYMPTOMS startet ///")
            print("\n")
            time.sleep(1)

            # Main game loop
            while self.year < 2100:
                self.trigger_event()
                self.count += 1
                if self.count == 5:
                    self.year += 1
                    self.count = 0
                    self.set_temperature()
                    print("┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄")
                    print(
                        f"JAHR {str(self.year)} - {float(self.temperature):.2}°C - {str(int(self.death_count))} TOTE - {len(self.occupied_regions)} AKTIVE REGION(EN)")
                    print("┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄")
                    # speichern_news("/year/", self.year)
                time.sleep(1)
            self.is_game_running = False
            time.sleep(1)
            print(f"SPIEL ZU ENDE: {str(int(self.death_count))} TOTE")
            time.sleep(4)

    def main(self, skip_headlines=False, verbose=False):
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
symptoms.main(skip_headlines=True, verbose=False)
