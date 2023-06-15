import random

terminology = dict({
    "na1": "an der amerikanischen Westküste",
    "na2": "an der amerikanischen Ostküste",
    "sa1": "an der Südküste von Südamerika",
    "sa2": "in Südamerika",
    "eu1": "in Europa",
    "af1": "in Westafrika",
    "af2": "im Nordosten Afrikas",
    "af3": "im Süden von Afrika",
    "as1": "in Indien",
    "as2": "in Nordostasien",
    "as3": "im Zentrum von Asien",
    "oc1": "in Ozeanien"
})


def construct_start_headline(region, catastrophe_type):
    region_term = terminology[region]
    if catastrophe_type == "hurricane":
        if region == "na1" or region == "na2":
            catastrophe_term = "Hurricane"
        elif region == "as1":
            catastrophe_term = "Zyklon"
        elif region == "as2":
            catastrophe_term = "Taifun"
        else:
            catastrophe_term = "Wirbelsturm"

        headlines = [
            "Großer " + catastrophe_term + " entsteht " + region_term,
            "Schlimme Prognosen: " + catastrophe_term + " " + region_term + " bedroht Tausende von Menschen",
            "Unwetter " + region_term + ": " + catastrophe_term + " entwickelt sich schnell",
            "Satellitenbilder zeigen: " + catastrophe_term + " " + region_term + " erreicht bald Festland",
            "Wissenschaftler warnen: " + catastrophe_term + " " + region_term + " wird Milliardenschaden anrichten",
            "Neuer " + catastrophe_term + " " + region_term + " wird bald Festland erreichen",
            catastrophe_term + " " + region_term + ": Experten fordern Evakuierung",
        ]
        return headlines[random.randrange(0, len(headlines) - 1)]
    elif catastrophe_type == "drought":
        headlines = [
            "Dürre " + region_term + " könnte Hungersnot auslösen",
            "Fehlender Niederschlag " + region_term + ": Dürre wird intensiver",
            "Kein Regen in Sicht: Dürre " + region_term,
            "Dürre " + region_term + ": Ausgangslage laut Experten 'unglaublich ungünstig'"
        ]
        return headlines[random.randrange(0, len(headlines) - 1)]
    else:
        return "Katastrophe vom Typ '" + catastrophe_type + "' " + region_term + " ausgebrochen"


def construct_end_headline(region, catastrophy_type, death_count):
    region_term = terminology[region]
    death_count_string = str(int(death_count))
    if catastrophy_type == "hurricane":
        if region == "na1" or region == "na2":
            catastrophe_term = "Hurricane"
        elif region == "as1":
            catastrophe_term = "Zyklon"
        elif region == "as2":
            catastrophe_term = "Taifun"
        else:
            catastrophe_term = "Wirbelsturm"

        headlines = [
            catastrophe_term + " " + region_term + " hat sich aufgelöst (" + death_count_string + " Tote)"
        ]
        return headlines[0]
    elif catastrophy_type == "drought":
        headlines = [
            "Regenfälle " + region_term + ": Dürreperiode ist zu Ende (" + death_count_string + " Tote)",
            "Schäden in Milliardenhöhe: Dürre " + region_term + " hinterlässt " + death_count_string + " Tote",
            "Dürreperiode " + region_term + " geht zu Ende: " + death_count_string + " Tote - Priester reden vom Willen Gottes"
            "Das Dürre-Drama " + region_term + " ist zu Ende: Regierung leugnet Opferzahlen (" + death_count_string + " Tote)"
        ]
        return headlines[random.randrange(0, len(headlines) - 1)]
    else:
        return "Katastrophe vom Typ '" + catastrophy_type + "' " + region_term + " is beendet (" + death_count_string + " Tote)"


def get_source():
    sources = ["Tiffany", "RAUM", "Norddeutsche Nachrichten", "Beuters", "New York Now", "HARE NEWS", "The Moon", "TON",
               "Erde", "APD", "Chicago Times", "The Protector", "The Impartial", "24 hourly Mail"]
    return random.choice(sources)
