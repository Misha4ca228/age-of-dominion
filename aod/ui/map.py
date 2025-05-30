import pygame
from aod.Class.Game import game
from aod.Class.State import state  # zoom и camera_offset здесь


def lighten_color(color, amount=40):
    return tuple(min(255, c + amount) for c in color)


def draw_map(surface, map_image_original, highlight_province=None):
    surface.fill((160, 160, 160))

    zoom = state.zoom
    offset = state.camera_offset

    scaled_size = [int(dim * zoom) for dim in map_image_original.get_size()]
    map_s = pygame.transform.smoothscale(map_image_original, scaled_size)
    surface.blit(map_s, offset)

    mouse_pos = pygame.mouse.get_pos()
    hovered = highlight_province

    if hovered is None:
        for prov_id, prov_data in game.map_provinces.items():
            verts = prov_data["vertices"]
            if len(verts) < 3:
                continue

            tpts = [(pygame.Vector2(p) * zoom + offset) for p in verts]
            xs = [p.x for p in tpts]
            ys = [p.y for p in tpts]
            rect = pygame.Rect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))



            if rect.collidepoint(mouse_pos):
                mask_surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
                shifted = [(p.x - rect.x, p.y - rect.y) for p in tpts]
                pygame.draw.polygon(mask_surf, (255, 255, 255, 255), shifted)

                local = (mouse_pos[0] - rect.x, mouse_pos[1] - rect.y)
                if 0 <= local[0] < rect.w and 0 <= local[1] < rect.h:
                    if mask_surf.get_at(local)[3] != 0:
                        hovered = prov_id
                        break


    for prov_id, prov_data in game.map_provinces.items():
        verts = prov_data["vertices"]
        if len(verts) < 3:
            continue

        owner = prov_data["owner"]
        base_color = game.scenario_countries[owner]["color"]
        col = lighten_color(base_color, 50) if prov_id == hovered or prov_id == game.dedicated_province else base_color
        tpts = [(pygame.Vector2(p) * zoom + offset) for p in verts]

        pygame.draw.polygon(surface, col, tpts)



        if zoom > 0.5:
            border_width = max(1, int(2 * zoom))
            pygame.draw.polygon(surface, (0, 0, 0), tpts, width=border_width)


    font = pygame.font.SysFont(None, int(14 * zoom))


    if zoom > 1:
        for prov_id, prov_data in game.map_provinces.items():
            verts = prov_data["vertices"]
            if len(verts) < 3:
                continue

            army = prov_data.get("army", 0)
            if army > 0:
                tpts = [(pygame.Vector2(p) * zoom + offset) for p in verts]
                center = sum(tpts, pygame.Vector2()) / len(tpts)

                text = font.render(str(army), True, (0, 0, 0))  # Можно сменить цвет при необходимости
                text_rect = text.get_rect(center=(center.x, center.y))
                surface.blit(text, text_rect)

    return hovered

def handle_map_click():

    if pygame.mouse.get_pressed()[0]:
        mods = pygame.key.get_mods()
        if mods & (pygame.KMOD_SHIFT | pygame.KMOD_CTRL | pygame.KMOD_ALT):
            return

        zoom = state.zoom
        offset = state.camera_offset
        mouse_pos = pygame.mouse.get_pos()

        for prov_id, prov_data in game.map_provinces.items():
            verts = prov_data["vertices"]
            if len(verts) < 3:
                continue

            tpts = [(pygame.Vector2(p) * zoom + offset) for p in verts]
            xs = [p.x for p in tpts]
            ys = [p.y for p in tpts]
            rect = pygame.Rect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))

            if rect.collidepoint(mouse_pos):
                mask_surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
                shifted = [(p.x - rect.x, p.y - rect.y) for p in tpts]
                pygame.draw.polygon(mask_surf, (255, 255, 255, 255), shifted)

                local = (mouse_pos[0] - rect.x, mouse_pos[1] - rect.y)
                if 0 <= local[0] < rect.w and 0 <= local[1] < rect.h:
                    if mask_surf.get_at(local)[3] != 0:
                        game.dedicated_province = prov_id
                        break

