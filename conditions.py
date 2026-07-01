"""
conditions.py  —  harsh "real world" conditions painted over the scene.  (shared, do NOT edit)

Each effect is applied to the whole scene BEFORE the camera crop is taken, so the model sees the
same rough weather the student sees. Effects use real image math (darkening, over-exposure,
gradient fog, and Gaussian sensor noise) so a clean-trained model has a genuinely hard time.
Only used when the app is started with  --hit-with-reality.
"""
import random
import numpy as np
import pygame

NAMES = ["Sunny", "Rainy", "Foggy", "Night", "Worn", "Random"]
RANDOM_SWITCH_FRAMES = 450     # Random flips condition every ~15 seconds (at 30 fps)


# ---------- full-frame numpy effects (operate on a float copy of the pixels) ----------
_grad_cache = {}


def _fog_grad(H):
    g = _grad_cache.get(H)
    if g is None:
        g = np.linspace(1.0, 0.5, H).reshape(1, H, 1).astype(np.float32)   # denser fog toward top
        _grad_cache[H] = g
    return g


def _noise(shape, sigma):
    """Fast Gaussian-ish noise, shared across the 3 colour channels (3x cheaper)."""
    if sigma <= 0:
        return None
    W, H, _ = shape
    s = int(sigma)
    return np.random.randint(-s, s + 1, size=(W, H, 1)).astype(np.float32)


def _foggy(a, k):
    alpha = np.clip(k * 0.95 * _fog_grad(a.shape[1]), 0.0, 0.95)
    a = a * (1 - alpha) + 232.0 * alpha
    n = _noise(a.shape, 30 * k)
    if n is not None:
        a = a + n
    return a


def _night(a, k):
    a = a * (1 - 0.82 * k)                                # darken a lot
    a[:, :, 2] += 22 * k                                  # cold blue cast
    n = _noise(a.shape, 20 * k)
    if n is not None:
        a = a + n
    return a


def _sunny(a, k):
    a = a * (1 + 1.15 * k)                                # over-expose / blow out highlights
    a = a * (1 - 0.32 * k) + 255.0 * (0.32 * k)           # wash toward white (low contrast)
    n = _noise(a.shape, 12 * k)
    if n is not None:
        a = a + n
    return a


def _rainy(a, k):
    a = a * (1 - 0.42 * k)                                # dim and grey
    n = _noise(a.shape, 28 * k)                           # heavy grain (wet, noisy lens)
    if n is not None:
        a = a + n
    return a


_NP = {"Foggy": _foggy, "Night": _night, "Sunny": _sunny, "Rainy": _rainy}


def _rain_streaks(surface, k):
    W, H = surface.get_size()
    rain = pygame.Surface((W, H), pygame.SRCALPHA)
    for _ in range(int(260 * k)):
        x = random.randint(0, W); y = random.randint(0, H)
        pygame.draw.line(rain, (205, 218, 238, 170), (x, y), (x - 5, y + 18), 1)
    surface.blit(rain, (0, 0))


def _worn_signs(surface, k, world):
    """Fade the sign colours and add dirt/scratches ON each sign.
    The pattern is FIXED per sign (seeded once), so it does not shimmer as the sign moves.
    The slider (k) controls how strong/opaque the wear looks, not the pattern."""
    W, H = surface.get_size()
    ov = pygame.Surface((W, H), pygame.SRCALPHA)
    signs = getattr(world, "signs", []) if world is not None else []
    for s in signs:
        cx, cy = int(s["x"]), int(s["y"])
        if cy < -60 or cy > H + 60:
            continue
        if "worn_seed" not in s:                          # give this sign one fixed pattern
            s["worn_seed"] = random.randint(0, 1_000_000)
        rng = random.Random(s["worn_seed"])               # same dirt every frame for THIS sign
        R = 52
        ov.fill((0, 0, 0, 0))
        pygame.draw.circle(ov, (185, 172, 150, int(160 * k)), (cx, cy), R)   # faded wash
        for _ in range(40):                               # a FIXED set of dirt spots
            dx = rng.randint(-R, R); dy = rng.randint(-R, R)
            if dx * dx + dy * dy > R * R:
                continue
            base = rng.choice([(55, 45, 35), (90, 78, 58), (150, 140, 118)])
            col = (base[0], base[1], base[2], int(190 * k))
            pygame.draw.circle(ov, col, (cx + dx, cy + dy), rng.randint(1, 4))
        for _ in range(6):                                # a FIXED set of scratches
            dx = rng.randint(-R, R); dy = rng.randint(-R, R)
            ex = dx + rng.randint(-22, 22); ey = dy + rng.randint(-8, 8)
            pygame.draw.line(ov, (70, 58, 45, int(170 * k)), (cx + dx, cy + dy), (cx + ex, cy + ey), 1)
        surface.blit(ov, (0, 0))


def apply(surface, name, intensity, frame=0, world=None):
    """Paint condition `name` (0-100 intensity) over the scene surface."""
    k = max(0.0, min(1.0, intensity / 100.0))
    if k <= 0 or name is None:
        return
    if name == "Random":
        pool = ["Foggy", "Night", "Sunny", "Rainy", "Worn"]
        name = pool[(frame // RANDOM_SWITCH_FRAMES) % len(pool)]

    if name == "Worn":
        _worn_signs(surface, k, world)
        return

    fn = _NP.get(name)
    if fn is None:
        return
    arr = pygame.surfarray.pixels3d(surface)              # live view (W, H, 3), uint8
    out = fn(arr.astype(np.float32), k)
    np.clip(out, 0, 255, out=out)
    arr[:, :, :] = out.astype(np.uint8)
    del arr                                               # unlock the surface
    if name == "Rainy":
        _rain_streaks(surface, k)
