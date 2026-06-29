"""
sim.py  —  the little traffic world (shared, you do NOT edit this).
The car has a CAMERA BOX (cyan square). Whatever is inside it is the image the
model sees and the image we save when recording.
"""
import os, math, random
import numpy as np
import pygame

W, H = 900, 620
ROAD_X, ROAD_W = 300, 300
CROP = pygame.Rect(360, 150, 180, 180)          # the camera patch on the road ahead

GRASS = (120, 170, 90); ROAD = (70, 72, 78); LANE = (240, 210, 80)
WHITE = (245, 245, 245); RED = (200, 45, 45); GREEN = (45, 175, 80)
DARK = (28, 31, 38); BLUE = (45, 95, 165); CYAN = (0, 190, 235)

CLASSES = ["Stop", "Speed25", "Speed55", "Red", "Green", "Nothing"]

# traffic light cycle (at ~30 fps): red for a while, then green, then red again...
LIGHT_RED_FRAMES = 180     # ~6 seconds red
LIGHT_GREEN_FRAMES = 270   # ~9 seconds green


def _text(surf, txt, cx, cy, size, color):
    f = pygame.font.SysFont("Arial", size, bold=True)
    img = f.render(txt, True, color)
    surf.blit(img, img.get_rect(center=(cx, cy)))


def draw_sign(surf, kind, cx, cy, scale=1.0):
    s = scale
    if kind == "Stop":
        r = int(46 * s)
        pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(22, 382, 45)]
        pygame.draw.polygon(surf, RED, pts)
        pygame.draw.polygon(surf, WHITE, pts, max(2, int(3 * s)))
        _text(surf, "STOP", cx, cy, int(19 * s), WHITE)
    elif kind in ("Speed25", "Speed55"):
        r = int(46 * s)
        pygame.draw.circle(surf, WHITE, (cx, cy), r)
        pygame.draw.circle(surf, RED, (cx, cy), r, max(3, int(6 * s)))
        _text(surf, kind[-2:], cx, cy, int(34 * s), DARK)
    elif kind in ("Red", "Green"):
        w, h = int(42 * s), int(98 * s)
        pygame.draw.rect(surf, DARK, (cx - w // 2, cy - h // 2, w, h), border_radius=int(8 * s))
        top = RED if kind == "Red" else (65, 65, 65)
        bot = GREEN if kind == "Green" else (65, 65, 65)
        pygame.draw.circle(surf, top, (cx, cy - int(23 * s)), int(13 * s))
        pygame.draw.circle(surf, bot, (cx, cy + int(23 * s)), int(13 * s))


class TrafficWorld:
    def __init__(self, headless=False, title="AI Car"):
        self.headless = headless
        if headless:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.display.init(); pygame.font.init()
        if headless:
            self.surface = pygame.Surface((W, H))
        else:
            self.surface = pygame.display.set_mode((W, H)); pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.dash = 0.0
        self.car_x = ROAD_X + ROAD_W // 2
        self.speed = 0.0
        self.signs = []
        self._last_spawn = None
        self.spawn_timer = 0
        self.frame = 0

    def light_phase(self):
        cycle = LIGHT_RED_FRAMES + LIGHT_GREEN_FRAMES
        return "Red" if (self.frame % cycle) < LIGHT_RED_FRAMES else "Green"

    def update(self):
        self.frame += 1
        phase = self.light_phase()
        self.dash = (self.dash + self.speed) % 40
        for s in self.signs:
            s["y"] += self.speed
            if s.get("light"):                 # a traffic light shows the current phase (red/green)
                s["kind"] = phase
        self.signs = [s for s in self.signs if s["y"] < H + 60]

        # only ONE sign may be near the camera box at a time (no overlap = clean training data)
        box_clear = (not self.signs) or (min(s["y"] for s in self.signs) > CROP.bottom + 20)
        self.spawn_timer -= 1
        if self.spawn_timer <= 0 and self.speed > 0.2 and box_clear:
            choices = [k for k in ["Stop", "Speed25", "Speed55", "Light"] if k != self._last_spawn]
            pick = random.choice(choices)                 # never the same thing twice in a row
            self._last_spawn = pick
            is_light = (pick == "Light")
            kind = phase if is_light else pick
            self.signs.append({"kind": kind, "light": is_light, "y": -60, "x": CROP.centerx, "scale": 1.0})
            self.spawn_timer = random.randint(25, 55)

    def apply(self, target_speed, steer):
        self.speed += (target_speed - self.speed) * 0.18
        if self.speed < 0.05:
            self.speed = 0.0
        self.car_x += steer * 4
        self.car_x = max(ROAD_X + 42, min(ROAD_X + ROAD_W - 42, self.car_x))

    def render_scene(self):
        s = self.surface
        s.fill(GRASS)
        pygame.draw.rect(s, ROAD, (ROAD_X, 0, ROAD_W, H))
        for y in range(-40, H, 40):
            pygame.draw.rect(s, LANE, (ROAD_X + ROAD_W // 2 - 4, y + int(self.dash), 8, 22))
        for sg in self.signs:
            draw_sign(s, sg["kind"], int(sg["x"]), int(sg["y"]), sg["scale"])
        self._car(s)

    def _car(self, s):
        cx, cy = int(self.car_x), 500
        pygame.draw.rect(s, BLUE, (cx - 26, cy - 40, 52, 80), border_radius=12)
        pygame.draw.rect(s, (185, 215, 245), (cx - 20, cy - 28, 40, 24), border_radius=6)
        for dx in (-26, 26):
            for dy in (-30, 30):
                pygame.draw.rect(s, (20, 20, 20), (cx + dx - 6, cy + dy - 12, 12, 24), border_radius=4)

    def draw_camera_box(self):
        """Draw the cyan box ON TOP — the model never sees this (we grab the crop first)."""
        pygame.draw.rect(self.surface, CYAN, CROP.inflate(8, 8), 3)
        _text(self.surface, "camera", CROP.centerx, CROP.top - 14, 16, CYAN)

    def _crop_surface(self, size):
        sub = self.surface.subsurface(CROP).copy()
        return pygame.transform.smoothscale(sub, (size, size))

    def save_crop(self, path, size=224):
        pygame.image.save(self._crop_surface(size), path)

    def get_crop_array(self, size):
        arr = pygame.surfarray.array3d(self._crop_surface(size))   # (w, h, 3) RGB
        return np.transpose(arr, (1, 0, 2)).copy()                 # (h, w, 3) RGB uint8
