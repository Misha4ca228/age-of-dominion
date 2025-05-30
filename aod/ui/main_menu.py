from aod.Class.Button import Button
from aod.Class.State import state
import pygame
import sys


def exit_game():
    pygame.quit()
    sys.exit()


def select_scenarios():
    state.state = "select_scenarios"


def pass_def():
    pass


def get_main_menu():
    return [
        Button("Новая игра", 0, 250, 180, 35, select_scenarios),
        Button("Загрузить игру", 0, 300, 180, 35, pass_def),
        Button("Покинуть игру", 0, 350, 180, 35, exit_game)
    ]


def main_menu_screen(events, screen, font, background_image):
    screen.blit(background_image, (0, 0))
    for event in events:

        for button in get_main_menu():
            button.check_click(event)

    for button in get_main_menu():
        button.draw(screen, font)
