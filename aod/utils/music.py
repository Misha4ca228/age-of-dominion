import os

import pygame
import random
from aod.Class.State import state

tracks = [f for f in os.listdir(state.music_folder) if f.endswith(state.supported_formats)]

current_track = random.choice(tracks)



def play_random_track():
    global current_track
    new_track = current_track
    while new_track == current_track and len(tracks) > 1:
        new_track = random.choice(tracks)
    current_track = new_track
    path = os.path.join(state.music_folder, current_track)
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    print(f"Играет: {current_track}")
