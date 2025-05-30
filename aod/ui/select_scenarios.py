import pygame

from aod.Class.Button import Button
from aod.Class.State import state
from aod.utils.Json import json_loader


def back_scenarios():
    if state.select_scenarios > 0:
        state.select_scenarios -= 1

def next_scenarios():
    scenarios_data = json_loader.load("maps/israel/scenarios/scenarios.json")
    scenarios_list = scenarios_data["scenarios"]
    if state.select_scenarios < len(scenarios_list) - 1:
        state.select_scenarios += 1


def select_country():
    state.state = "select_country"



def get_select_scenarios():
    return [
        Button("<<", 265, 700, 170, 35, back_scenarios),
        Button("Далее", 465, 700, 170, 35, select_country),
        Button(">>", 665, 700, 170, 35, next_scenarios)
    ]


def select_scenarios_screen(events, screen, font, background_image):
    scenarios_data = json_loader.load(f"maps/israel/scenarios/scenarios.json")
    scenarios_list = scenarios_data["scenarios"]
    scenario = scenarios_list[state.select_scenarios]
    scenario_photo = f"{json_loader.get_project_path("aod", "maps", "israel", "scenarios", scenario, "preview.png")}"
    scenario_info = json_loader.load(f"maps/israel/scenarios/{scenario}/scenario.json")
    state.select_scenario = scenario

    screen.blit(background_image, (0, 0))

    preview_image = pygame.image.load(scenario_photo).convert_alpha()
    screen.blit(preview_image, (294, 170))

    text_surface = font.render(f"Название: {scenario_info['name']}", True, (0, 0, 0))
    screen.blit(text_surface, (294, 100))


    for event in events:
        for button in get_select_scenarios():
            button.check_click(event)


    for button in get_select_scenarios():
        button.draw(screen, font)
