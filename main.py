import pygame
import sys

from aod.Class.State import state
from aod.ui.main_menu import main_menu_screen
from aod.ui.map import draw_map, handle_map_click
from aod.ui.province_info import render_province_info
from aod.ui.select_country import select_country_screen
from aod.ui.select_scenarios import  select_scenarios_screen

pygame.init()
screen = pygame.display.set_mode((1100, 800))
pygame.display.set_caption("Menu and Simple Game Example")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 30)

background_image = pygame.image.load("aod/resources/image/bg.png").convert()
background_image = pygame.transform.scale(background_image, (1100, 800))

background_image2 = pygame.image.load("map.png").convert()
background_image2 = pygame.transform.scale(background_image2, (935, 930))

min_zoom = 0.1
max_zoom = 5

running = True
while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                state.dragging = True
                state.last_mouse_pos = pygame.Vector2(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                state.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if state.dragging and state.state == "game":
                mouse_pos = pygame.Vector2(event.pos)
                delta = mouse_pos - state.last_mouse_pos
                state.camera_offset += delta
                state.last_mouse_pos = mouse_pos

        elif event.type == pygame.MOUSEWHEEL:
            old_zoom = state.zoom
            if event.y > 0:
                state.zoom *= 1.1
            else:
                state.zoom /= 1.1
            state.zoom = max(min_zoom, min(max_zoom, state.zoom))

            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            state.camera_offset -= (mouse_pos - state.camera_offset) * (state.zoom / old_zoom - 1)

    if state.state == "game":
        handle_map_click()
        draw_map(surface=screen, map_image_original=background_image2)
        render_province_info(screen)

    elif state.state == "main_menu":
        main_menu_screen(events, screen, font, background_image)

    elif state.state == "select_scenarios":
        select_scenarios_screen(events, screen, font, background_image)

    elif state.state == "select_country":
        select_country_screen(events, screen, font, background_image)




    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

