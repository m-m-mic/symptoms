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
    elif catastrophe_type == "flooding":
        headlines = [
            "Anhaltende Überschwemmung " + region_term + ", Gefahr vor kontaminierten Wasser nimmt rasant zu",
            "Starker Niederschlag " + region_term + ": Überschwemmungen nehmen zu",
            "Anhaltender Starkregen: Überschwemmung " + region_term,
            "Nach Starkregen " + region_term + " sind die Staudämme an ihren Grenzen",
            "Platzregen gemischt mit Hagel " + region_term + " setzten der Umwelt sehr zu",
            "Überschwemmungen sorgten " + region_term + " zu Erdrutschen, Anwohner werden evakuiert",
            "Aktuelle Warnung: Tiefdruckgebiet" + region_term + "verstärkt sich"
        ]
        return headlines[random.randrange(0, len(headlines) - 1)]
    elif catastrophe_type == "earthquake":
        headlines = [
            "Starkes Erdbeben " + region_term + " erschüttert Einwohner",
            "Erdbeben " + region_term + ": Keine Aussicht auf Rettung?",
            "Ungewöhnlich hohe Stärke: Erdbeben " + region_term,
            "Erdbeben " + region_term + ": Ganze Orte evakuiert"
        ]
        return headlines[random.randrange(0, len(headlines) - 1)]
    elif catastrophe_type == "tsunami":
        headlines = [
            "Tsunami Warnung " + region_term + ": Experten fordern sofortige Evakuierung",
            "Panik " + region_term + " - Große Tsunamiwelle bewegt sich auf Festland zu",
            "Schlimme Prognosen: Tsunami " + region_term + " gefährdet tausende von Menschen",
            "Nach nächtlichem Unterwasserbeben - Tsunami " + region_term + " erreicht bald Festland",
            "Sofortige Evakuierung notwendig! Tsunamiwelle " + region_term + " bedroht unzählige Siedelungen"
        ]
        return headlines[random.randrange(0, len(headlines) - 1)]
    elif catastrophe_type == "sandstorm":
        headlines = [
            "Sandsturmwarnung: Die Straßen in " + region_term + " werden zur Gafehrenzone",
            "Achtung! Wegen eines Sandsturms sollten Bürger in " + region_term + " heute Zuhause bleiben",
            "Massiver Sandsturm in " + region_term + ". Sofortige Maßnahmen der Regierung nötig",
            "Verheerender Sandsturm: " + region_term + " erlebt Katastrophe",
            "Jahrunderts Sandsturm!" + region_term + " muss sofort evakuiert werden!"
        ]
        return headlines[random.randrange(0, len(headlines) - 1)]
    else:
        return "Katastrophe vom Typ '" + catastrophe_type + "' " + region_term + " ausgebrochen"


def construct_end_headline(region, catastrophy_type, death_count):
    region_term = terminology[region]
    death_count_string = f"{int(death_count):,}"
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
            catastrophe_term + " " + region_term + " hat sich aufgelöst (" + death_count_string + " Tote)",
            death_count_string + " Tote und überall Zerstörung - " + catastrophe_term + " " + region_term + " offiziell zu Ende",
            catastrophe_term + " Katastrophe " + region_term + ": Regierungen berichten von " + death_count_string + " Toten",
            "Ende von " + catastrophe_term + " " + region_term + " - " + death_count_string + " Opfer"
        ]
        return headlines[random.randrange(0, len(headlines) - 1)]
    elif catastrophy_type == "drought":
        headlines = [
            "Regenfälle " + region_term + ": Dürreperiode ist zu Ende (" + death_count_string + " Tote)",
            "Schäden in Milliardenhöhe: Dürre " + region_term + " hinterlässt " + death_count_string + " Tote",
            "Dürreperiode " + region_term + " geht zu Ende: " + death_count_string + " Tote - Priester reden vom Willen Gottes",
            "Das Dürre-Drama " + region_term + " ist zu Ende: Regierung leugnet Opferzahlen (" + death_count_string + " Tote)",
        ]
        return headlines[random.randrange(0, len(headlines) - 1)]
    elif catastrophy_type == "flooding":
        headlines = [
            "Entwarnung: Wasser " + region_term + " ist wieder trinkbar, " + death_count_string + " Menschen starben an den Folgen",
            "Tiefdruck " + region_term + " löst sich auf (" + death_count_string + " Tote)",
            "Starkregen " + region_term + "hat immens an Kraft verloren: Bisher kam es zu " + death_count_string + " Toten",
            "Anwohner im Gebiet der Staudammbereich " + region_term + " evakuiert, " + death_count_string + " Tote und unzählige Vermisste",
            "Aufatmen! Platzregen " + region_term + " hat gestoppt (" + death_count_string + " Tote)",
            "Die letzten Anwohner im Erdrutschgebiet wurden evakuiert: Die Anzahl der Toten liegt bei " + death_count_string,
            "Tiefdruckgebiet " + region_term + " löst sich auf (" + death_count_string + " Tote)"
        ]
        return headlines[random.randrange(0, len(headlines) - 1)]
    elif catastrophy_type == "earthquake":
        headlines = [
            "Erdbeben " + region_term + " hinterlässt Spuren (" + death_count_string + " Tote)",
            "Zerstörte Häuser " + region_term + ": Erdbeben endlich zu Ende,  " + death_count_string + " Tote",
            "Erdbeben " + region_term + " geht zu Ende: " + death_count_string + " Tote - Gläubige reden vom Willen Gottes",
            "Nach Erdbeben " + region_term + " : " + death_count_string + " Tote - alles kaputt!",
            "Erdbeben " + region_term + " geht zu Ende: " + death_count_string + " Tote - Gläubige reden vom Willen Gottes",
            "Erdbeben " + region_term + " : 'Ich dachte, der Boden bricht unter mir ein' - " + death_count_string + " Tote"
        ]
        return headlines[random.randrange(0, len(headlines) - 1)]
    elif catastrophy_type == "tsunami":
        headlines = [
            "Tsunami " + region_term + " lässt zerstörerische Spuren zurück: " + death_count_string + " Tote",
            death_count_string + " Opfer durch Tsunami " + region_term + ": Wissenschaftler fordern Konsequenzen in der Politik",
            "Traumatische Szenen " + region_term + ": Tsunami Opferzahlen steigen zu " + death_count_string
        ]
        return headlines[random.randrange(0, len(headlines) - 1)]
    elif catastrophy_type == "sandstorm":
        headlines = [
            "Sandsturm  " + region_term + " fordert " + death_count_string + " Tote. Experten sagen die Regierung hat viel zu spät reagiert",
            death_count_string + " starben durch katastrophalen Sandsturm. " + region_term + " entsetzt",
            "Ein Sandsturm in " + region_term + " verursachte " + death_count_string + " Tote. Zu späte Maßnahmen führten zu massenhaft Unfällen",
            region_term + " verwüstet durch Sandsturm. Die Bürger trauern um " + death_count_string + " Tote."
        ]
        return headlines[random.randrange(0, len(headlines) - 1)]
    else:
        return "Katastrophe vom Typ '" + catastrophy_type + "' " + region_term + " ist beendet (" + death_count_string + " Tote)"


def get_source():
    sources = ["Tiffany", "RAUM", "Norddeutsche Nachrichten", "Beuters", "New York Now", "HARE NEWS", "The Moon", "TON",
               "Erde", "APD", "Chicago Times", "The Protector", "The Impartial", "24 hourly Mail"]
    return random.choice(sources)
