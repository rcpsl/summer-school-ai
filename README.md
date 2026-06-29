# Wednesday — Make the car drive itself

On Monday your model learned to **recognize** signs. Today you make it **drive** the
car: stop at stop signs, obey speed limits, and go on green. You'll finish the
**`brain.py`** Controller. Read this whole page — it tells you exactly what to write.

You only edit **`brain.py`**.

---

## The class names (same as Monday)
```
Stop    Speed25    Speed55    Red    Green    Nothing
```

## 0) Set up + bring your model
- Use the same conda env: `conda activate trafficsim`
- Put your Monday **`model_unquant.tflite`** and **`labels.txt`** in this folder.

## 1) Run it
```bash
python wednesday_app.py
```
- Click **Mode** to switch **MANUAL ↔ AUTO**.
  - **MANUAL** — hold the **UP arrow** to drive (let go to stop).
  - **AUTO** — the model drives. (AUTO is **gray/disabled** until a model is in the folder.)
- Press **Q** to quit.

Run it now in **AUTO** before editing — the car drives, but speed and turning won't be
right yet, because you haven't finished the Controller.

---

## 2) What the car SHOULD do (the behavior you're building)
- **Speed signs set a *lasting* limit.** When it sees **Speed55**, it should go at 55 and
  **keep** going 55 — past empty road, green lights, everything — until it sees **Speed25**,
  then it goes 25 and keeps it. (A speed limit stays until a new speed sign changes it.)
- **Arrows steer.** `Left` → steer left, `Right` → steer right (only if you trained those).
- **Stop sign** → stop, wait ~2 seconds, then drive on.
- **Red light** → stop until it turns **Green**, then go.

## 3) Your job — finish `Controller.update()` in `brain.py`
There are exactly **two TODOs**. The hard "waiting" part is already written for you (it's
explained in section 4 so you understand it).

**TODO 1 — the lasting speed limit.** A speed sign should change `self.limit`:
```python
if label in SPEED_LIMITS:
    self.limit = SPEED_LIMITS[label]     # SPEED_LIMITS = {"Speed25": 25, "Speed55": 55}
```
Because `self.limit` only changes here, it naturally *stays the same* until the next speed sign.

**TODO 2 — how fast and which way.** Turn the limit into a speed, and read arrows:
```python
cruise = self.limit / 10.0                                   # e.g. 55 -> 5.5 pixels/frame
steer  = -1 if label == "Left" else (1 if label == "Right" else 0)
```

Save and run `python wednesday_app.py` in AUTO. The bottom bar shows `speed 25/55`, and the
car should hold its limit until a new speed sign.

---

## 4) How the "waiting" logic works (this part is GIVEN to you)
A red light and a stop sign behave **differently**, so the Controller treats them differently:

- **Red light → wait for green.** While the model sees `Red`, the car stays at speed 0. The
  traffic light turns **green on its own** after several seconds; the moment the model sees
  `Green`, the car drives on. (A real red light makes you wait however long it takes.)
- **Stop sign → timed stop.** When the car sees `Stop`, it stops for `HOLD` seconds (2 s), then
  drives on. A `COOLDOWN` (5 s) then makes it *ignore* that stop sign so it can roll past without
  stopping over and over on the same one.

To do this the Controller has two states, **DRIVE** and **STOPPED**, and it remembers whether it
stopped for a *stop sign* (use the 2-second timer) or for a *red light* (wait for green).

> **Want a challenge?** Try writing this part yourself from the description above. Otherwise leave
> the given code as-is — it already works.

---

## 5) Tuning (optional, in the files)
- `brain.py`: `Controller.HOLD` (wait time), `Controller.COOLDOWN` (time before it can stop again),
  `SPEED_LIMITS`, `DEFAULT_LIMIT`.
- `brain.py`: `CONFIDENCE_THRESHOLD` (ignore weak guesses), `DEBOUNCE_FRAMES` (steadiness).

## 6) Troubleshooting
- **Car ignores everything / never stops** → the label names must be exactly
  `Stop, Speed25, Speed55, Red, Green, Nothing`. Check the bottom bar: does it literally say `Stop`?
- **Speed shows the wrong number / always 35** → finish **TODO 1** (the limit isn't being set).
- **It crawls / stops over and over at a stop sign** → make sure you didn't change the given
  waiting logic; the cooldown is what lets it drive past.
- **AUTO is gray** → no model in the folder. Add `model_unquant.tflite` + `labels.txt` and restart.
