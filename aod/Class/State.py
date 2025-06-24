import pygame

from aod.utils.Json import json_loader


class State:
    def __init__(self, state="main_menu", select_scenarios=0, select_country=0):
        self.state = state
        self.select_scenarios = select_scenarios
        self.select_scenario = None
        self.select_country = select_country
        self.player_country = None

        self.music_folder = f"{json_loader.get_project_path()}/aod/resources/musics"
        self.supported_formats = (".mp3", ".ogg", ".wav")

        self.zoom = 1
        self.camera_offset = pygame.Vector2(0, 0)

        self.dragging = False
        self.last_mouse_pos = None

state = State()
