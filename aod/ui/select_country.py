import pygame

from aod.Class.Button import Button
from aod.Class.Game import game
from aod.Class.State import state
from aod.utils.Json import json_loader
from aod.utils.countries import filter_countries


def back_country():
    if state.select_country > 0:
        state.select_country -= 1

def next_country():
    countries = json_loader.load(f"maps/israel/scenarios/{state.select_scenario}/scenario.json")
    scenario_countries = list(countries["participants"].keys())
    if state.select_country < len(scenario_countries) - 1:
        state.select_country += 1


def start():
    state.state ="game"
    all_countries = json_loader.load(f"game/countries.json")

    participants = json_loader.load(f"maps/israel/scenarios/{state.select_scenario}/scenario.json")
    country_ids = list(participants["participants"].keys())
    game.scenario_countries = filter_countries(country_ids, all_countries)
    game.player_country = state.player_country


def get_select_scountry():
    return [
        Button("<<", 265, 700, 170, 35, back_country),
        Button("Играть", 465, 700, 170, 35, start),
        Button(">>", 665, 700, 170, 35, next_country)
    ]




def select_country_screen(events, screen, font, background_image):
    scenario_info = json_loader.load(f"maps/israel/scenarios/{state.select_scenario}/scenario.json")
    scenario_countries = list(scenario_info["participants"].keys())
    country = scenario_countries[state.select_country]
    country_info = json_loader.load(f"game/countries.json")[country]
    flag = f"{json_loader.get_project_path("aod", "resources", "flags", country_info["flag"])}"

    state.player_country = country
    print(country)
    screen.blit(background_image, (0, 0))

    preview_image = pygame.image.load(flag).convert_alpha()
    screen.blit(preview_image, (294, 350))

    text_surface = font.render(f"{country_info['name']}", True, (0, 0, 0))
    screen.blit(text_surface, (294, 100))


    for event in events:
        for button in get_select_scountry():
            button.check_click(event)


    for button in get_select_scountry():
        button.draw(screen, font)
