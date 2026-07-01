"""
ui.py  —  tiny on-screen buttons, a slider, and a status bar. (shared, do NOT edit)
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
        f = pygame.font.SysFont("Arial", 16, bold=True)
        img = f.render(self.text, True, WHITE)
        surf.blit(img, img.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.enabled and self.rect.collidepoint(pos)


class Slider:
    """A 0-100 slider. Click or drag anywhere on the track to set the value."""
    def __init__(self, x, y, w, value=60, label="Harshness"):
        self.x = x; self.y = y; self.w = w
        self.value = value
        self.label = label

    def draw(self, surf):
        pygame.draw.rect(surf, (205, 210, 218), (self.x, self.y + 9, self.w, 6), border_radius=3)
        filled = int(self.w * self.value / 100)
        pygame.draw.rect(surf, (15, 163, 199), (self.x, self.y + 9, filled, 6), border_radius=3)
        knob_x = int(self.x + self.w * self.value / 100)
        pygame.draw.circle(surf, (15, 163, 199), (knob_x, self.y + 12), 9)
        f = pygame.font.SysFont("Arial", 15, bold=True)
        surf.blit(f.render(f"{self.label}: {int(self.value)}%", True, (30, 40, 60)), (self.x, self.y - 15))

    def grab(self, pos):
        """If pos is near the track, set the value and return True."""
        if self.x - 8 <= pos[0] <= self.x + self.w + 8 and self.y - 8 <= pos[1] <= self.y + 26:
            self.value = max(0, min(100, 100 * (pos[0] - self.x) / self.w))
            return True
        return False


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
