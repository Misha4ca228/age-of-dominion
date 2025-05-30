from aod.utils.Json import json_loader


class Game:
    def __init__(self):
        self.map_provinces = json_loader.load(f"maps/israel/provinces.json")
        self.scenario_countries = {}
        self.player_country = None
        self.dedicated_province = "1"

game = Game()