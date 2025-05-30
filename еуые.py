import pygame
import json
import sys

# === Константы ===
WIDTH, HEIGHT = 1100, 800
BG_COLOR = (30, 30, 30)
POLYGON_COLOR = (0, 255, 0, 200)        # текущий полигон (полупрозрачный)
OTHER_POLYGON_COLOR = (100, 100, 100, 200)  # остальные (более прозрачные)

# === Инициализация Pygame и экрана ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Province Polygon Editor with Map + Zoom + Pan")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# === Загрузка карты и данных провинций ===
map_image = pygame.image.load("map.png").convert()  # после set_mode!
orig_w, orig_h = map_image.get_size()

with open("provinces.json", "r", encoding="utf-8") as f:
    provinces = json.load(f)

# === Состояние редактора ===
current_id = None
current_points = []

zoom = 1.0
min_zoom, max_zoom = 0.5, 3.0
camera_offset = pygame.Vector2(0, 0)
dragging = False
last_mouse_pos = None
input_text = ""

# === Функции ===
def draw_polygon_alpha(surface, color, points):
    """Рисует полигон с прозрачностью через глобальный zoom и offset."""
    if len(points) < 3:
        return
    tmp = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    transformed = [(pygame.Vector2(p) * zoom + camera_offset) for p in points]
    pygame.draw.polygon(tmp, color, transformed)
    surface.blit(tmp, (0, 0))

def save_provinces():
    with open("provinces.json", "w", encoding="utf-8") as f:
        json.dump(provinces, f, ensure_ascii=False, indent=4)
    print("Saved provinces.json")

# === Главный цикл ===
while True:
    screen.fill(BG_COLOR)

    # 1) Масштаб и панорамирование карты
    scaled_size = (int(orig_w * zoom), int(orig_h * zoom))
    map_scaled = pygame.transform.smoothscale(map_image, scaled_size)
    screen.blit(map_scaled, camera_offset)

    # 2) Рисуем все существующие полигоны (кроме текущего)
    for pid, pdata in provinces.items():
        verts = pdata.get("vertices", [])
        if len(verts) < 3 or pid == current_id:
            continue
        draw_polygon_alpha(screen, OTHER_POLYGON_COLOR, verts)

    # 3) Рисуем текущий полигон
    if current_points:
        draw_polygon_alpha(screen, POLYGON_COLOR, current_points)
        for p in current_points:
            sp = pygame.Vector2(p) * zoom + camera_offset
            pygame.draw.circle(screen, (0, 200, 0), (int(sp.x), int(sp.y)), max(3, int(3 * zoom)))

    # 4) Подсказки
    if current_id:
        screen.blit(font.render(f"ID={current_id}  Zoom={zoom:.2f}", True, (255,255,255)), (10,10))
        screen.blit(font.render("ЛКМ: добавить точку | Enter: сохранить | Del: очистить | Esc: выйти", True, (255,255,255)), (10,40))
    else:
        screen.blit(font.render("Введите ID и нажмите Enter:", True, (255,255,255)), (10,10))
        screen.blit(font.render(input_text, True, (255,255,255)), (10,40))

    # Обработка событий
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif e.type == pygame.KEYDOWN:
            if not current_id:
                if e.key == pygame.K_RETURN:
                    if input_text in provinces:
                        current_id = input_text
                        current_points = provinces[current_id].get("vertices", []).copy()
                    else:
                        print(f"Province ID '{input_text}' not found")
                    input_text = ""
                elif e.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif e.unicode.isdigit():
                    input_text += e.unicode
            else:
                if e.key == pygame.K_RETURN:
                    provinces[current_id]["vertices"] = current_points.copy()
                    save_provinces()
                elif e.key == pygame.K_DELETE:
                    current_points = []
                elif e.key == pygame.K_ESCAPE:
                    current_id = None
                    current_points = []

        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1 and current_id:
                mp = pygame.Vector2(e.pos)
                wp = (mp - camera_offset) / zoom
                current_points.append([int(wp.x), int(wp.y)])
            elif e.button == 3:
                dragging = True
                last_mouse_pos = pygame.Vector2(e.pos)

        elif e.type == pygame.MOUSEBUTTONUP:
            if e.button == 3:
                dragging = False

        elif e.type == pygame.MOUSEMOTION:
            if dragging:
                mp = pygame.Vector2(e.pos)
                camera_offset += (mp - last_mouse_pos)
                last_mouse_pos = mp

        elif e.type == pygame.MOUSEWHEEL:
            old_zoom = zoom
            zoom = max(min_zoom, min(max_zoom, zoom * (1.1 if e.y > 0 else 0.9)))
            mp = pygame.Vector2(pygame.mouse.get_pos())
            camera_offset -= (mp - camera_offset) * (zoom / old_zoom - 1)

    pygame.display.flip()
    clock.tick(60)
