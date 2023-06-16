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
import tkinter

# UPD Client for world map visualisation
client = udp_client.SimpleUDPClient("127.0.0.1", 12000)

# Imports Catastrophe class
from catastrophe import Catastrophe

# Gets headline constructors
from construct_headline import construct_start_headline, construct_end_headline, get_source

# Loads in .env file which needs to be located in the same folder as this file
load_dotenv()
# Fetches api key from .env file (can be generated at https://platform.openai.com/account/api-keys)
openai.api_key = os.getenv("OPENAI_API_KEY")

# UPD Client for world map visualisation
client = udp_client.SimpleUDPClient("127.0.0.1", 7000)

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
                "type": "",
                "resolution_percentage": 0,
            },
            "na2": {
                "is_active": False,
                "type": "",
                "resolution_percentage": 0,
            },
            "eu1": {
                "is_active": False,
                "type": "",
                "resolution_percentage": 0,
            },
            "sa1": {
                "is_active": False,
                "type": "",
                "resolution_percentage": 0,
            },
            "sa2": {
                "is_active": False,
                "type": "",
                "resolution_percentage": 0,
            },
            "af1": {
                "is_active": False,
                "type": "",
                "resolution_percentage": 0,
            },
            "af2": {
                "is_active": False,
                "type": "",
                "resolution_percentage": 0,
            },
            "af3": {
                "is_active": False,
                "type": "",
                "resolution_percentage": 0,
            },
            "as1": {
                "is_active": False,
                "type": "",
                "resolution_percentage": 0,
            },
            "as2": {
                "is_active": False,
                "type": "",
                "resolution_percentage": 0,
            },
            "as3": {
                "is_active": False,
                "type": "",
                "resolution_percentage": 0,
            },
            "oc1": {
                "is_active": False,
                "type": "",
                "resolution_percentage": 0,
            },
        }
        self.headline_reserve = []
        self.used_headlines = []
        self.sensor_values: list[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.has_first_catastrophe_happened = False
        self.annihilation_triggered = False

    def reset_attributes(self):
        generated_headlines = self.headline_reserve
        self.__init__()
        self.headline_reserve = generated_headlines

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

    def send_data(self):
        tick_count = 0
        while True:
            if tick_count > 5:
                # Sends data to p5project
                client.send_message('/death_count', round(self.death_count))
                tick_count = 0
            tick_count += 1

            region_json = json.dumps(self.region_data, indent=4)
            client.send_message("/region_data", region_json)

            client.send_message("/is_game_running", self.is_game_running)
            time.sleep(0.1)

    def generate_headlines(self, verbose):
        while True:
            if len(self.headline_reserve) < 100:
                if verbose:
                    print("Filling up headlines... (currently " + str(len(self.headline_reserve)) + "/100)")
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
                        self.headline_reserve.append({"headline": headline, "source": get_source()})
                    # Rests for 5 seconds
                    time.sleep(5)
                except Exception as e:
                    # Catches bad response from GPT API
                    print("Error while generating headlines:", e)

    def set_temperature(self):
        # Temperature graph
        self.temperature = 1.5 * math.cos(0.04 * (self.year - self.start_year) + math.pi) + 2.5

    def trigger_headline(self):
        if len(self.headline_reserve) > 0:
            # Randomly picks headline from array
            index = random.randrange(0, len(self.headline_reserve))
            headline = self.headline_reserve[index]
            print(headline["headline"] + " - " + headline["source"])

            self.used_headlines.insert(0, headline)
            # Removes chosen headline from array
            del self.headline_reserve[index]
        else:
            print("--- Blank (headline) ---")

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
            self.used_headlines.insert(0, start_headline)
            print(
                "════════════════════════════════════════════════════════════════════════════════════════════════════════════")
            print(
                f"!!! CATASTROPHE - {selected_region} - {catastrophe.type} - {float(catastrophe.wind_up):.3}s wind_up - {float(catastrophe.duration):.3}s dur - {float(catastrophe.resolution_time):.3}s res_time - {int(catastrophe.deaths_per_second):,} d_p_s !!!")
            print(start_headline["headline"] + " - " + start_headline["source"])
            print("!!! On electrode " + str(catastrophe.electrode_index) + " - " + key_mapping[
                catastrophe.electrode_index] + " !!!")
            print(
                "════════════════════════════════════════════════════════════════════════════════════════════════════════════")

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
            self.used_headlines.insert(0, end_headline)
            print(
                "════════════════════════════════════════════════════════════════════════════════════════════════════════════")
            print(
                f">>> RESOLVED - {selected_region} - {catastrophe.type} - resolved by player? {resolved_by_player} <<<")
            print(end_headline["headline"] + " - " + end_headline["source"])
            print(
                "════════════════════════════════════════════════════════════════════════════════════════════════════════════")

            if self.is_game_running is True:
                # Puts region on 2 second cooldown
                time.sleep(2)

            # Moves region back from occupied to free
            self.free_regions.append(selected_region)
            self.occupied_regions.remove(selected_region)
        else:
            print("--- Blank (catastrophe) ---")

    def trigger_annihilation(self):
        print("☁☢☁ Started annihilation event ☁☢☁")
        # Occupies regions until it reaches four occupied
        war_regions = []
        while len(war_regions) < 4:
            if len(self.free_regions) > 0:
                selected_region = self.free_regions[0]
                self.free_regions.remove(selected_region)
                self.occupied_regions.add(selected_region)
                print(f"☁☢☁ Added {selected_region} to annihilation event ☁☢☁")
                war_regions.append(selected_region)

        # Gets sensor value indexes for all four occupied regions
        region_indexes = []
        for region in war_regions:
            catastrophe = Catastrophe(region, self.temperature)
            region_indexes.append(catastrophe.electrode_index)
            self.region_data[region]["is_active"] = True
            self.region_data[region]["type"] = "annihilation"
            self.region_data[region]["resolution_percentage"] = 0

        # Constructs starting headline for the nuclear war
        start_headline = {
            "headline": "Nach Monaten der Anspannung - DEFCON 1 erreicht: Das Zeitalter der Atomkriege beginnt",
            "source": "Tiffany"
        }
        print(
            "☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢")
        print(f"☢☢☢ NUCLEAR WAR - {str(war_regions)} ☢☢☢")
        print(start_headline["headline"] + " - " + start_headline["source"])
        print("☢☢☢ On electrodes " + str(region_indexes) + " ☢☢☢")
        print(
            "☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢")

        # Sets starting parameters for annihilation
        resolution_time = 4
        deaths_per_second = 500_000_000
        current_death_count = 0
        current_resolution_time = 0

        # Annihilation loop which runs until death_count reaches 10 billion, the game ends or the player resolves the event
        while self.death_count < 10_000_000_000 and self.is_game_running is True:
            if self.sensor_values[region_indexes[0]] > 100 and self.sensor_values[region_indexes[1]] > 100 and \
                    self.sensor_values[region_indexes[2]] > 100 and self.sensor_values[region_indexes[3]] > 100:
                current_resolution_time += 0.01
                for region in war_regions:
                    self.region_data[region][
                        "resolution_percentage"] = current_resolution_time / resolution_time
            if current_resolution_time >= resolution_time:
                break
            self.death_count += deaths_per_second * 0.01
            current_death_count += deaths_per_second * 0.01
            time.sleep(0.01)

        # Changes region data
        for region in war_regions:
            self.region_data[region]["is_active"] = False

        # Sends ending headline
        end_headline = {
            "headline": f"Ein Wunder: Der Atomkrieg ist vorbei! Für den Frieden mussten nur {int(current_death_count):,} Personen sterben",
            "source": "Tiffany"
        }
        print(
            "☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢")
        print(end_headline["headline"] + " - " + end_headline["source"])
        print(
            "☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢☁☢")

        if self.is_game_running is True:
            # Puts regions on 2 second cooldown
            time.sleep(2)

        # Moves regions back from occupied to free
        for region in war_regions:
            self.free_regions.append(region)
            self.occupied_regions.remove(region)

    def trigger_event(self):
        # Chance of nuclear war
        chance_annihilation = 0.001 * (self.death_count / 10_000_000)
        # Limits chance of nuclear war to 10 %
        if chance_annihilation > 0.08:
            chance_annihilation = 0.08
        # Prevents further nuclear wars if one has already been triggered
        if self.annihilation_triggered is True:
            chance_annihilation = 0
        # Chance of headline occurring
        chance_headline = 0.25
        # Base chance of catastrophe occurring
        base_chance_catastrophe = 0.10
        # Temperature increase since game start
        temperature_delta = self.temperature - 1
        # Chance of nothing happening
        chance_remaining = 1 - chance_headline - base_chance_catastrophe - chance_annihilation
        # Chance of catastrophe occurring depending on temperature
        catastrophe_function = 0.7 * (math.cos(math.pi + (temperature_delta / 3) * math.pi) + 1)
        if catastrophe_function > 1:
            catastrophe_function = 1
        chance_catastrophe = base_chance_catastrophe + catastrophe_function * chance_remaining
        # Increase chance of first catastrophe
        if self.has_first_catastrophe_happened is False:
            chance_catastrophe = 0.5

        # Picks random number
        random_number = random.randrange(0, 1000000) / 1000000

        # Triggers headline
        if random_number < chance_headline:
            self.trigger_headline()

        # Triggers catastrophe
        elif random_number < (chance_headline + chance_catastrophe):
            self.has_first_catastrophe_happened = True
            Thread(target=self.trigger_catastrophe).start()

        elif random_number < (chance_headline + chance_catastrophe + chance_annihilation):
            if self.annihilation_triggered is False:
                self.annihilation_triggered = True
                Thread(target=self.trigger_annihilation).start()

        # Triggers nothing
        else:
            print("--- Blank ---")

    def run(self, skip_headlines):
        while True:
            # Game starts when any of the sensors are touched by the player
            print("\nTouch any electrode to start game.\n")
            while self.is_game_running is False:
                if any(sensor > 100 for sensor in self.sensor_values):
                    # Clears all attributes except headlines
                    self.reset_attributes()
                    self.is_game_running = True
                    break

            # Waits for headline generation until at least 20 are available
            if len(self.headline_reserve) < 20 and not skip_headlines:
                print("Waiting for GPT to return headlines...\n")
            while len(self.headline_reserve) < 20 and not skip_headlines:
                pass

            print("/// SYMPTOMS startet ///")
            print("\n")
            time.sleep(1)

            # Main game loop
            while self.year < 2100 and self.death_count < 10_000_000_000:
                self.trigger_event()
                self.count += 1
                if self.count == 5:
                    self.year += 1
                    self.count = 0
                    self.set_temperature()
                    print("┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄")
                    print(
                        f"JAHR {self.year} - {float(self.temperature):.2}°C - {int(self.death_count):,} TOTE - {len(self.occupied_regions)} AKTIVE REGION(EN) - ATOMKRIEG WAHRSCHEINLICHKEIT {(0.01 * (self.death_count / 10_000_000)):.2%}")
                    print("┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄")
                time.sleep(1)
            self.is_game_running = False
            time.sleep(1)
            if self.death_count >= 10_000_000_000:
                print(f"\n// MENSCHHEIT AUSGESTORBEN, SPIEL ZU ENDE: {int(self.death_count):,} TOTE //")
            else:
                print(f"\n// SPIEL ZU ENDE: {int(self.death_count):,} TOTE //")
                if self.annihilation_triggered:
                    print("★ DU HAST DIE ZERSTÖRUNG DER MENSCHHEIT DURCH DEN ATOMKRIEG VERHINDERT. GUT GEMACHT! ★")
            time.sleep(4)

    def gui(self):
        def update_labels():
            # @Melli tkinter benutzt jetzt statt der txt-Datei direkt die Attribute der Klasse, sonst ist es quasi gleich
            year_label.config(text=str(self.year))
            temperature_label.config(text=f"{self.temperature:.2f} °C")
            death_count_label.config(text=f"{int(self.death_count):,}")

            headlines_to_display = self.used_headlines[:15]
            headlines_text = "\n".join(headlines_to_display)
            headline_list_label.config(text=headlines_text)

            window.after(100, update_labels)

        window = tkinter.Tk()

        # Label for year variable
        year_label = tkinter.Label(window, text=str(self.year), bg="white", font=("Arial", 18))
        year_label.pack(fill=tkinter.X)

        # Label for temperature variable
        temperature_label = tkinter.Label(window, text=f"{self.temperature:.2f} °C", bg="white", font=("Arial", 12))
        temperature_label.pack(fill=tkinter.Y, side=tkinter.RIGHT)

        # Label for death count TODO: @Melli wahrscheinlich den entfernen, da er auf der Karte angezeigt wird?
        death_count_label = tkinter.Label(window, text=f"{int(self.death_count):,}", bg="white", font=("Arial", 12))
        death_count_label.pack(fill=tkinter.X)

        # Label for the list of headlines
        headline_list_label = tkinter.Label(window, bg="white", font=("Arial", 12))
        headline_list_label.pack(fill=tkinter.X)

        update_labels()
        window.mainloop()

    def main(self, skip_headlines=False, verbose=False):
        # Starts GUI with headlines, year & temperature
        Thread(target=self.gui).start()

        # Headline generation thread
        if not skip_headlines:
            Thread(target=self.generate_headlines, args=(verbose,)).start()

        # Input fetching thread
        Thread(target=self.get_inputs, daemon=True).start()

        # Sends data to p5
        Thread(target=self.send_data, daemon=True).start()

        # Runtime thread
        Thread(target=self.run, args=(skip_headlines,)).start()


symptoms = Symptoms()

# Props:
# skip_headlines: Whether headline generation is skipped (defaults to False)
# verbose: Prints progress of headline generation (defaults to True)
symptoms.main(skip_headlines=True, verbose=False)
