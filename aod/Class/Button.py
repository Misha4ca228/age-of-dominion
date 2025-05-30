import pygame


class Button:
    def __init__(self, text, x, y, width, height, action):
        self.text = text
        self.action = action
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface, font):
        mouse = pygame.mouse.get_pos()
        color = (100, 100, 100) if self.rect.collidepoint(mouse) else (60, 60, 60)
        pygame.draw.rect(surface, color, self.rect)
        label = font.render(self.text, True, (255, 255, 255))
        surface.blit(label, label.get_rect(center=self.rect.center))

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if callable(self.action):
                self.action()
