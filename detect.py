"""
detect.py  —  the DETECTION half of the self-driving car.   (STUDENT)

  1) predict_label()  — this is your finished Monday code (already done for you).
  2) Debouncer        — YOUR MORNING TASK: finish add_frame() so the label becomes steady.
"""
import numpy as np

THRESHOLD = 0.6     # ignore guesses the model isn't at least this sure about


def predict_label(probs, labels):
    """Return the name of the highest-scoring class (or 'Nothing' if unsure)."""
    best = int(np.argmax(probs))
    if float(probs[best]) < THRESHOLD:
        return "Nothing"
    return labels[best]


class Debouncer:
    """
    Smooths out the model's flicker.

    From frame to frame the model can wobble: for the SAME speed sign it might say
    "Speed55", "Speed25", "Speed55", "Speed55". If the car reacted to every single
    frame it would jerk around. The Debouncer keeps the last few labels and only
    TRUSTS a label once the whole window agrees. That trusted label is the "action".
    """

    def __init__(self, window_size=4):
        self.window_size = window_size      # how many frames in a row must agree
        self.observed_frames = []           # recent labels, e.g. ["Speed55", "Speed55", "Speed25"]
        self.action = "Nothing"             # the steady label we currently trust

    def add_frame(self, new_label):
        """
        Add this frame's label to the window, then return the STEADY action.

        `self.observed_frames` is a list of the most recent labels, for example:
            ["Speed55", "Speed55", "Speed25"]

        Two list tools you will use:

            self.observed_frames.append("Speed55")     # add to the END
                ["Speed55","Speed55","Speed25"]  ->  ["Speed55","Speed55","Speed25","Speed55"]

            self.observed_frames.pop(0)                # remove the FIRST (oldest)
                ["Speed55","Speed55","Speed25","Speed55"]  ->  ["Speed55","Speed25","Speed55"]

        What to write (steps 1-4):
            1) add `new_label` to the end of self.observed_frames
            2) if self.observed_frames is longer than self.window_size, remove the oldest one
            3) check every label in self.observed_frames. If they are ALL the same,
               set self.action to that label.
                 Tip: start with   all_the_same = True
                      then use a    for   loop over self.observed_frames;
                      if any label is different from the first one, set all_the_same = False.
            4) return self.action
        """

        # ----- write steps 1 to 4 here -----

        return self.action     # (this line is fine to keep as the last line)
