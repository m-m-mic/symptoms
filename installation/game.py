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
        self.didGameEnd = False
        self.startYear = 2025
        self.year = self.startYear
        self.count = 1
        self.deathCount = 0
        self.temperature = 1
        self.regions = ["na1", "na2", "eu1", "eu2", "sa1", "sa2", "me1", "af1", "af2", "as1", "as2", "oc1"]
        self.occupiedRegions = set()
        self.headlines = []

    def generateHeadlines(self):
        while len(self.headlines) < 100:
            print("Generating headlines... (" + str(len(self.headlines)) + "/100)")
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user",
                     "content": "Generiere 25 kurze, fiktive & sarkastische Schlagzeilen über den Klimawandel. Die Schlagzeilen sollen keine Jahreszahlen oder den Begriff Klimawandel beinhalten. Geb die Schlagzeilen als Liste mit dem key 'headlines' in einer JSON zurück"}
                ]
            )
            try: 
                headlines_json = json.loads(completion.choices[0].message.content)
                for headline in headlines_json['headlines']:
                    self.headlines.append(headline)
            except: 
                print('GPT returned wrong data format')

    def getTemperature(self):
        self.temperature = 1.5*math.cos(0.04*(self.year-self.startYear)+math.pi)+2.5
        print(self.temperature)

    def triggerHeadline(self):
        if len(self.headlines) > 0:
            index = random.randrange(0, len(self.headlines))
            print(self.headlines[index])
            del self.headlines[index]
        else:
            print("Ran out of headlines :((((")
        
    def triggerCatastrophe(self):
        catastrophes = ['drought', 'hurricane', 'flood', 'wildfire', 'sandstorm']
        catastrophe = random.choice(catastrophes)
        print(f'Oh no! A {catastrophe}  ＼(º □ º l|l)/')
    
    def triggerEvent(self):
        headlineChance = 0.25
        startingCatastropheChance = 0.10
        tempIncrease = self.temperature - 1
        restChance = 1 - headlineChance - startingCatastropheChance
        catastrChance = startingCatastropheChance + (math.cos(math.pi + (tempIncrease / 3) * math.pi) + 1) * restChance

        randomNumber = random.randrange(0, 101) / 100

        if(randomNumber < headlineChance):
            self.triggerHeadline()
        elif(randomNumber < (headlineChance + catastrChance)):
            self.triggerCatastrophe()

    def run(self):
        self.didGameEnd = False
        if len(self.headlines) == 0:
            self.generateHeadlines()
        while self.year < 2100:
            self.triggerEvent()
            self.count += 1
            if self.count == 6:
                self.year += 1
                print(self.year)
                self.count = 1
                self.getTemperature()
            time.sleep(1)
        self.didGameEnd = True
        self.generateHeadlines()


sym = Symptoms()
sym.run()