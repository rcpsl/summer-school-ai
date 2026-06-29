"""
brain.py  —  the driving decision code.  (STUDENT version)

classify() and Debouncer are done for you (you wrote classify on Monday).
You will finish the Controller — see the two TODOs. The README explains the
whole control idea step by step, including the waiting logic that is given to you.
"""
import time
import numpy as np

CONFIDENCE_THRESHOLD = 0.6
DEBOUNCE_FRAMES = 4


def classify(probs, labels, threshold=CONFIDENCE_THRESHOLD):
    i = int(np.argmax(probs))
    conf = float(probs[i])
    if conf < threshold:
        return "UNSURE", conf
    return labels[i], conf


class Debouncer:
    def __init__(self, frames=DEBOUNCE_FRAMES):
        self.frames = frames
        self.recent = []
        self.committed = "Nothing"

    def push(self, label):
        self.recent.append(label)
        if len(self.recent) > self.frames:
            self.recent.pop(0)
        if len(self.recent) == self.frames and all(x == self.recent[0] for x in self.recent):
            self.committed = self.recent[0]
        return self.committed


SPEED_LIMITS = {"Speed25": 25, "Speed55": 55}
DEFAULT_LIMIT = 35


class Controller:
    HOLD = 2.0          # seconds to wait at a stop sign / red light
    COOLDOWN = 5.0      # seconds to ignore stop/red after going (so we drive past the sign)

    def __init__(self):
        self.state = "DRIVE"
        self.t_stop = 0.0
        self.cooldown_until = 0.0
        self.limit = DEFAULT_LIMIT     # current speed limit (25 / 35 / 55)
        self._stop_sign = False        # True while we are stopped AT A STOP SIGN (not a red light)

    def update(self, label, now=None):
        now = time.time() if now is None else now

        # ============================ TODO 1 ============================
        # PERSISTENT SPEED LIMIT.
        # If `label` is a speed sign, change self.limit to its number.
        #   Hint:   if label in SPEED_LIMITS:
        #               self.limit = SPEED_LIMITS[label]
        # (write those two lines here)

        # ============================ TODO 2 ============================
        # HOW FAST and WHICH WAY.
        # Replace the two lines below using these hints:
        #   cruise = self.limit / 10.0
        #   steer  = -1 if label == "Left" else (1 if label == "Right" else 0)
        cruise = 3.5     # <-- replace using the hint
        steer = 0        # <-- replace using the hint
        # ===============================================================

        # ---- the waiting logic is GIVEN to you (the README explains how it works) ----

        # RED LIGHT: wait here; go the moment it is no longer red (it turns green by itself).
        if label == "Red":
            self.state = "STOPPED"
            self._stop_sign = False
            return (0.0, 0)

        # STOP SIGN: stop for HOLD seconds, then drive past (COOLDOWN stops it re-stopping).
        if self.state == "STOPPED" and self._stop_sign:
            if now - self.t_stop >= self.HOLD:
                self.state = "DRIVE"
                self._stop_sign = False
                self.cooldown_until = now + self.COOLDOWN
                return (cruise, 0)          # done waiting: drive on at the current limit
            return (0.0, 0)                 # keep waiting
        if label == "Stop" and now >= self.cooldown_until:
            self.state = "STOPPED"
            self._stop_sign = True
            self.t_stop = now
            return (0.0, 0)                 # start the stop

        self.state = "DRIVE"
        return (cruise, steer)              # normal driving

    def display_speed(self):
        return 0 if self.state == "STOPPED" else self.limit
