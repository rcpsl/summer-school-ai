"""
ui.py  —  tiny on-screen buttons and a status bar (shared, you do NOT edit this).
"""
import pygame

GRAYBTN = (120, 128, 140); ONBTN = (40, 170, 80); OFFBTN = (45, 95, 165)
BAR = (16, 35, 63); WHITE = (255, 255, 255)


class Button:
    def __init__(self, x, y, w, h, text, enabled=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.enabled = enabled
        self.on = False

    def draw(self, surf):
        bg = GRAYBTN if not self.enabled else (ONBTN if self.on else OFFBTN)
        pygame.draw.rect(surf, bg, self.rect, border_radius=8)
        f = pygame.font.SysFont("Arial", 17, bold=True)
        img = f.render(self.text, True, WHITE)
        surf.blit(img, img.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.enabled and self.rect.collidepoint(pos)


def draw_buttons(surf, buttons):
    for b in buttons:
        b.draw(surf)


def draw_statusbar(surf, lines, height=70):
    w = surf.get_width(); h = surf.get_height()
    ov = pygame.Surface((w, height)); ov.set_alpha(228); ov.fill(BAR)
    surf.blit(ov, (0, h - height))
    f = pygame.font.SysFont("Arial", 19, bold=True)
    y = h - height + 8
    for line in lines:
        surf.blit(f.render(line, True, WHITE), (16, y))
        y += 24
