# Wednesday — Make the Car Drive Itself

Today you turn Monday's model into a **driver**. It's a full-day build in two parts:

- **Morning — steady detection.** Finish the **Debouncer** in `detect.py` so the model's
  guess stops flickering.
- **Afternoon — decisions.** Finish the **Controller** in `brain.py` so the car decides how
  fast to go (stop signs, red lights, speed limits).

You only edit **`detect.py`** and **`brain.py`**.

---

## 0) Set up
- Get the code: scan the QR and switch to the branch **`week2_wednesday`** (see the slides).
- `conda activate trafficsim`
- Put your **Monday** `model_unquant.tflite` and `labels.txt` in this folder.
- Run it: `python wednesday_app.py`
  - **Mode** button → MANUAL (hold **UP** to drive) or AUTO (the model drives; gray until a model is present).
  - **Record** button → save camera pictures into `frames/` (same as Monday), in case you want more training images.
  - The bottom bar shows: `sees <raw label>  ->  action <steady label>  |  speed <n>`.

## The files
| File | You edit? | What it holds |
|------|-----------|---------------|
| `detect.py` | ✅ (morning) | `predict_label` (your Monday code, done) **+ the Debouncer** |
| `brain.py`  | ✅ (afternoon) | the **Controller** (`decide_speed`) |
| `wednesday_app.py`, `sim.py`, `ui.py`, `tm_model.py` | ❌ | the app and simulator |

---

# MORNING — The Debouncer (`detect.py`)

## Why we need it
The model **flickers**. Looking at the *same* 55 sign it might say, frame by frame:

```
Speed55, Speed25, Speed55, Speed55
```

If the car reacted to every single frame it would jerk — briefly slowing for the fake `Speed25`.
The Debouncer keeps the **last few** labels and only **trusts** a label once the whole window
agrees. That trusted label is called the **action**.

## What `add_frame(new_label)` does
`self.observed_frames` is a list of the most recent labels, e.g. `["Speed55", "Speed55", "Speed25"]`.

Two list tools you'll use:

```python
self.observed_frames.append("Speed55")   # add to the END
#   ["Speed55","Speed55","Speed25"]  ->  ["Speed55","Speed55","Speed25","Speed55"]

self.observed_frames.pop(0)              # remove the FIRST (oldest)
#   ["Speed55","Speed55","Speed25","Speed55"]  ->  ["Speed55","Speed25","Speed55"]
```

Write these four steps in `add_frame`:

1. **Add** `new_label` to the end of `self.observed_frames`.
2. If the list is longer than `self.window_size`, **remove the oldest** one.
3. Check if **every** label in the list is the same. If so, set `self.action` to that label.
   - Tip: start with `all_the_same = True`, then use a **`for`** loop over `self.observed_frames`;
     if any label is different from the first one, set `all_the_same = False`.
4. **Return** `self.action`.

## Test it — the flicker test bench
Run this to check your Debouncer against a deliberately jumpy label stream (no model needed):

```bash
python wednesday_app.py --test-flickering
```

The camera shows a sign that flickers (Speed55 → Speed25 → Speed55 …). Watch the bottom bar:

- **CAMERA sees (flickering)** jumps around every frame.
- **ACTION (steady)** should **stay put** during the flicker, and only change after a **solid run of 4**
  identical frames.

If `ACTION` jumps around too, your `add_frame` isn't smoothing yet — go back and finish steps 1–4.

---

# AFTERNOON — The Controller (`brain.py`)

`decide_speed(action, now)` returns **one number**: the target speed (`0` means stop). It follows
three rules. (No steering yet — that's for the real car.)

## Rule 1 — Speed limit (it STAYS)
A speed sign sets the limit; nothing else changes it:

```python
if action == "Speed25":
    self.speed_limit = 25
if action == "Speed55":
    self.speed_limit = 55
normal_speed = self.speed_limit / 10.0     # e.g. 55 -> 5.5
```
Because you only change `self.speed_limit` here, a 55 limit **stays 55** through empty road and
green lights until a `Speed25` sign appears.

## Rule 2 — Red light (wait for green)
```python
if action == "Red":
    return 0
```
Stay stopped while it's red. When the light turns green the action becomes `"Green"`, so this rule
stops applying and the car drives.

## Rule 3 — Stop sign (a TIMED stop)
A stop sign is different from a red light: you stop for a couple of seconds and then **go**, even if
the sign is still there. You have these helpers (already set up in `__init__`):

- `self.waiting_at_stop` — True/False: are we sitting at a stop sign now?
- `self.stop_started_time` — the time we started waiting
- `self.ignore_stop_until` — ignore stop signs until this time
- `self.SECONDS_TO_WAIT_AT_STOP` (2 s), `self.SECONDS_TO_IGNORE_STOP` (3 s)
- `now` — the current time in seconds

The logic, in words:

- **If we are already waiting** at a stop sign: figure out how long we've waited
  (`now - self.stop_started_time`). If it's **less** than `SECONDS_TO_WAIT_AT_STOP`, keep waiting
  (`return 0`). Otherwise we're done: set `self.waiting_at_stop = False`, set
  `self.ignore_stop_until = now + self.SECONDS_TO_IGNORE_STOP`, and drive on (`return normal_speed`).
- **If we see a NEW stop sign** (`action == "Stop"`) **and** we're past the ignore time
  (`now >= self.ignore_stop_until`): begin the stop — set `self.waiting_at_stop = True`, set
  `self.stop_started_time = now`, and `return 0`.

**Why the ignore time?** When the car stops, the sign freezes in the camera box. After we start
driving again we must ignore that sign for a few seconds so we roll **past** it — otherwise we'd
stop on it over and over.

## Rule 4 — Otherwise
`return normal_speed`.

## Test it
In **AUTO** the car should: hold a speed limit until a new speed sign; **stop ~2 s** at a stop sign
then drive on; and **wait at a red light** until it turns green.

---

## Tuning
- `detect.py`: `window_size` — bigger = steadier but slower to react.
- `brain.py`: `SECONDS_TO_WAIT_AT_STOP`, `SECONDS_TO_IGNORE_STOP`, `DEFAULT_SPEED_LIMIT`.

## Troubleshooting
- **Ignores every sign** → the labels must be exactly `Stop, Speed25, Speed55, Red, Green, Nothing`.
  Watch the `sees` value on the bottom bar.
- **Speed is always 35** → Rule 1 isn't done (the limit never changes).
- **Jumpy / reacts to a single blip** → finish the Debouncer, or raise `window_size`.
- **AUTO is gray** → no model in the folder; add your files and restart.
