import random


class Catastrophe:
    def __init__(self, region, temperature):
        self.__region_catastrophes = {
            "na1": ["hurricane", "drought"],
            "na2": ["hurricane", "wildfire"],
            "eu1": ["hurricane", "drought"],
            "sa1": ["hurricane", "wildfire"],
            "sa2": ["hurricane", "drought"],
            "af1": ["hurricane", "wildfire"],
            "af2": ["hurricane", "drought"],
            "af3": ["hurricane", "wildfire"],
            "as1": ["hurricane", "drought"],
            "as2": ["hurricane", "wildfire"],
            "as3": ["hurricane", "drought"],
            "oc1": ["hurricane", "wildfire"],
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
                    "max": 200
                }
            },
            "hurricane": {
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
                    "max": 200
                }
            },
            "drought": {
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
                    "max": 200
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
        wind_up = random.randrange(catastrophe_data["wind_up"]["min"], catastrophe_data["wind_up"]["max"])
        # get deaths_per_second
        deaths_per_second = random.randrange(catastrophe_data["deaths_per_second"]["min"],
                                             catastrophe_data["deaths_per_second"]["max"]) * temperature
        # get resolution_time
        resolution_time = random.randrange(catastrophe_data["resolution_time"]["min"],
                                           catastrophe_data["resolution_time"]["max"]) * temperature
        return duration, wind_up, deaths_per_second, resolution_time
