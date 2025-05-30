import pygame

from aod.Class.Game import game
from aod.utils.Json import json_loader


def render_province_info(screen):
    prov_id = game.dedicated_province
    prov_data = game.map_provinces[prov_id]
    font = pygame.font.Font(None, 20)
    countries = game.scenario_countries
    owner_name =  countries[prov_data["owner"]]["name"]
    flag = countries[prov_data["owner"]]["flag"]



    pygame.draw.rect(screen, (200, 200, 200),
                     (0, 700, 400, 100))

    flag_image = pygame.image.load(json_loader.get_project_path("aod", "resources", "flags", flag)).convert_alpha()
    flag_image = pygame.transform.scale(flag_image, (50, 25))

    screen.blit(flag_image, (20, 705))


    pop_image = pygame.image.load(json_loader.get_project_path("aod", "resources", "image", "population.png")).convert_alpha()
    screen.blit(pop_image, (20, 735))

    economy_image = pygame.image.load(
        json_loader.get_project_path("aod", "resources", "image", "economy.png")).convert_alpha()
    screen.blit(economy_image, (20, 755))

    army_image = pygame.image.load(
        json_loader.get_project_path("aod", "resources", "image", "army.png")).convert_alpha()
    screen.blit(army_image, (20, 775))

    up = pygame.image.load(
        json_loader.get_project_path("aod", "resources", "image", "up.png")).convert_alpha()
    screen.blit(up, (130, 735))

    text_name = font.render(f"{owner_name} | {prov_data["name"]}", True, (0, 0, 0))
    screen.blit(text_name, (75, 710))

    text_pop = font.render(f"{prov_data["population"]}", True, (0, 111, 8))
    screen.blit(text_pop, (47, 737))

    text_economy = font.render(f"{prov_data["economy"]}", True, (160, 126, 0))
    screen.blit(text_economy, (47, 757))

    text_army = font.render(f"{prov_data["army"]}", True, (0, 0, 0))
    screen.blit(text_army, (47, 777))

    up_name = font.render(f"{round(prov_data["growth"]*100, 2)}%", True, (0, 0, 0))
    screen.blit(up_name, (140, 735))
