import random


class Catastrophe:
    def __init__(self, region, temperature):
        self.__region_catastrophes = {
            "na1": ["hurricane", "drought", "wildfire", "earthquake"],
            "na2": ["hurricane", "wildfire", "flooding"],
            "eu1": ["wildfire", "drought", "flooding"],
            "sa1": ["wildfire", "tsunami", "earthquake"],
            "sa2": ["wildfire", "flooding"],
            "af1": ["sandstorm", "drought"],
            "af2": ["sandstorm", "drought"],
            "af3": ["drought", "wildfire"],
            "as1": ["hurricane", "drought", "tsunami", "flooding"],
            "as2": ["hurricane", "wildfire", "tsunami", "earthquake", "flooding"],
            "as3": ["wildfire", "drought", "sandstorm"],
            "oc1": ["wildfire", "drought", "tsunami", "earthquake"],
        }
        self.__region_electrode = ["na1", "na2", "eu1", "sa1", "sa2", "af1", "af2", "af3", "as1", "as2", "as3", "oc1"]
        self.__catastrophe_data = {
            "wildfire": {
                "duration": {
                    "min": 4,
                    "max": 7
                },
                "wind_up": {
                    "min": 1,
                    "max": 3,
                },
                "deaths_per_second": {
                    "min": 200,
                    "max": 600
                },
                "resolution_time": {
                    "min": 1,
                    "max": 80
                }
            },
            "hurricane": {
                "duration": {
                    "min": 4,
                    "max": 7
                },
                "wind_up": {
                    "min": 0,
                    "max": 3
                },
                "deaths_per_second": {
                    "min": 500,
                    "max": 900
                },
                "resolution_time": {
                    "min": 30,
                    "max": 80
                }
            },
            "drought": {
                "duration": {
                    "min": 5,
                    "max": 10
                },
                "wind_up": {
                    "min": 1,
                    "max": 7
                },
                "deaths_per_second": {
                    "min": 200,
                    "max": 1100
                },
                "resolution_time": {
                    "min": 1,
                    "max": 120
                }
            },
            "tsunami": {
                "duration": {
                    "min": 2,
                    "max": 5
                },
                "wind_up": {
                    "min": 0,
                    "max": 1,
                },
                "deaths_per_second": {
                    "min": 4000,
                    "max": 10000
                },
                "resolution_time": {
                    "min": 1,
                    "max": 40
                }
            },
            "flooding": {
                "duration": {
                    "min": 2,
                    "max": 7
                },
                "wind_up": {
                    "min": 1,
                    "max": 6,
                },
                "deaths_per_second": {
                    "min": 200,
                    "max": 500000
                },
                "resolution_time": {
                    "min": 1,
                    "max": 120
                }
            },
            "sandstorm": {
                "duration": {
                    "min": 2,
                    "max": 6
                },
                "wind_up": {
                    "min": 1,
                    "max": 3,
                },
                "deaths_per_second": {
                    "min": 200,
                    "max": 2000
                },
                "resolution_time": {
                    "min": 1,
                    "max": 40
                }
            },
            "earthquake": {
                "duration": {
                    "min": 1,
                    "max": 4
                },
                "wind_up": {
                    "min": 0,
                    "max": 1
                },
                "deaths_per_second": {
                    "min": 1500,
                    "max": 6000
                },
                "resolution_time": {
                    "min": 1,
                    "max": 70
                }
            }
        }
        self.type = self.get_type(region)
        self.electrode_index = self.get_electrode_index(region)
        self.duration, self.wind_up, self.deaths_per_second, self.resolution_time = self.get_catastrophe_attributes(
            temperature)

    def get_type(self, region):
        # gets a random catastrophe for the region
        types = self.__region_catastrophes[region]
        return random.choice(types)

    def get_electrode_index(self, region):
        # gets electrode index which is connected to the region
        return self.__region_electrode.index(region)

    def get_catastrophe_attributes(self, temperature):
        catastrophe_data = self.__catastrophe_data[self.type]
        # get duration
        duration = random.randrange(catastrophe_data["duration"]["min"],
                                    catastrophe_data["duration"]["max"]) * temperature
        # get wind_up
        wind_up = random.randrange(catastrophe_data["wind_up"]["min"], catastrophe_data["wind_up"]["max"]) / temperature
        # get deaths_per_second
        deaths_per_second = random.randrange(catastrophe_data["deaths_per_second"]["min"],
                                             catastrophe_data["deaths_per_second"]["max"]) * (temperature**temperature*1.2)
        # get resolution_time
        resolution_time = random.randrange(catastrophe_data["resolution_time"]["min"],
                                           catastrophe_data["resolution_time"]["max"]) * temperature / 100
        
        # prevents resolution_time from being longer than catastrophe itself
        if resolution_time > wind_up + duration:
            resolution_time = (wind_up + duration) * 0.8
        
        # prevents resolution_time from being longer than 6 seconds
        if resolution_time > 6:
            resolution_time = 6

        return duration, wind_up, deaths_per_second, resolution_time
