"""
detect.py  —  turn the model's scores into a label.   (STUDENT version)

This is the ONLY file you need to change today.
Follow the two TODOs below. The README explains exactly what to write.
"""
import numpy as np

THRESHOLD = 0.6     # ignore guesses the model isn't this sure about


def predict_label(probs, labels):
    # `probs`  = a list of scores, one per class, that add up to 1
    # `labels` = the class names, in the same order as the scores
    #
    # ============================ TODO 1 ============================
    # Find the position (index) of the BIGGEST score.
    #   Hint:   best = int(np.argmax(probs))
    best = 0          # <-- replace this line using the hint
    #
    # ============================ TODO 2 ============================
    # (optional) If the biggest score is too small, we aren't sure.
    # If  probs[best]  is less than  THRESHOLD , return "Nothing".
    #   Hint:   if float(probs[best]) < THRESHOLD: return "Nothing"
    #
    # ===============================================================
    return labels[best]
