import math
import time
import random
import openai
import json
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


class Symptoms:
    def __init__(self):
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

    def generate_headlines(self):
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
                print('GPT returned wrong data format')

    def get_temperature(self):
        self.temperature = 1.5 * math.cos(0.04 * (self.year - self.start_year) + math.pi) + 2.5
        print(self.temperature)

    def trigger_headline(self):
        if len(self.headlines) > 0:
            index = random.randrange(0, len(self.headlines))
            print(self.headlines[index])
            del self.headlines[index]
        else:
            print("Ran out of headlines :((((")

    def trigger_catastrophe(self):
        catastrophes = ['drought', 'hurricane', 'flood', 'wildfire', 'sandstorm']
        catastrophe = random.choice(catastrophes)
        print(f'Oh no! A {catastrophe}  ＼(º □ º l|l)/')

    def trigger_event(self):
        chance_headline = 0.25
        base_chance_catastrophe = 0.10
        temperature_delta = self.temperature - 1
        chance_remaining = 1 - chance_headline - base_chance_catastrophe
        chance_catastrophe = base_chance_catastrophe + (math.cos(math.pi + (temperature_delta / 3) * math.pi) + 1) * chance_remaining
        random_number = random.randrange(0, 101) / 100

        if random_number < chance_headline:
            self.trigger_headline()
        elif random_number < (chance_headline + chance_catastrophe):
            self.trigger_catastrophe()

    def run(self):
        self.did_game_end = False
        if len(self.headlines) == 0:
            self.generate_headlines()
        while self.year < 2100:
            self.trigger_event()
            self.count += 1
            if self.count == 6:
                self.year += 1
                print(self.year)
                self.count = 1
                self.get_temperature()
            time.sleep(1)
        self.did_game_end = True
        self.generate_headlines()


symptoms = Symptoms()
symptoms.run()
