"""
brain.py  —  the CONTROL half of the self-driving car.   (STUDENT)

The detection code (detect.py) gives us a steady "action" each moment, one of:
    "Stop", "Red", "Green", "Speed25", "Speed55", "Nothing".

YOUR AFTERNOON TASK: finish decide_speed() so the car follows three rules:
    1. Speed limit  — a speed sign sets a limit that STAYS until a new speed sign.
    2. Red light    — stop and wait; drive again once it is green.
    3. Stop sign    — stop for a couple of seconds, then drive on.

No steering yet. decide_speed() returns ONE number: the target speed (0 = stopped).
Read the README section "The Controller" — it explains every step. Then fill the TODOs.
"""

DEFAULT_SPEED_LIMIT = 35     # the limit before we have seen any speed sign


class Controller:
    SECONDS_TO_WAIT_AT_STOP = 2.0     # how long to sit still at a stop sign
    SECONDS_TO_IGNORE_STOP  = 6.0     # after leaving a stop sign, ignore stops this long

    def __init__(self):
        self.speed_limit = DEFAULT_SPEED_LIMIT   # current limit: 25, 35, or 55
        self.waiting_at_stop = False             # are we sitting at a stop sign right now?
        self.stop_started_time = 0.0             # the time we began waiting at the stop sign
        self.ignore_stop_until = 0.0             # ignore stop signs until this time

    def decide_speed(self, action, now):
        """
        Return the car's target speed this frame (0 = stopped).
          action : the steady label from the Debouncer
          now    : the current time in seconds
        """

        # STEP 1 — SPEED LIMIT (a speed sign changes it; otherwise it stays).
        # TODO: if action is "Speed25", set self.speed_limit to 25
        #       if action is "Speed55", set self.speed_limit to 55
        normal_speed = self.speed_limit / 10.0        # e.g. 55 -> 5.5

        # STEP 2 — RED LIGHT: stop and wait.
        # TODO: if action is "Red", return 0
        #       (when the light turns green the action becomes "Green", so this stops applying)

        # STEP 3 — STOP SIGN: a TIMED stop. Use these helpers:
        #     self.waiting_at_stop        True/False: are we sitting at a stop sign now?
        #     self.stop_started_time      the time we started waiting
        #     self.ignore_stop_until      ignore stop signs until this time
        #     self.SECONDS_TO_WAIT_AT_STOP , self.SECONDS_TO_IGNORE_STOP
        #     now                         the current time in seconds
        #

        if self.waiting_at_stop:
            # TODO 3a: if we are ALREADY waiting at a stop sign (self.waiting_at_stop is True):
            #            - work out how long we have waited:  now - self.stop_started_time
            #            - if that is LESS than SECONDS_TO_WAIT_AT_STOP  ->  return 0  (keep waiting)
            #            - otherwise we are done waiting:
            #                 set self.waiting_at_stop = False
            #                 set self.ignore_stop_until = now + SECONDS_TO_IGNORE_STOP
            #                 return normal_speed            (drive on)
            #
            waited_time = now - self.stop_started_time
            pass
        
        elif action == "Stop" and now >= self.ignore_stop_until:
            # TODO 3b: if we see a NEW stop sign (action is "Stop") AND now >= self.ignore_stop_until:
            #            - set self.waiting_at_stop = True
            #            - set self.stop_started_time = now
            #            - return 0                          (begin the stop)
            pass


        # STEP 4 — nothing special: drive at the normal speed.
        return normal_speed
