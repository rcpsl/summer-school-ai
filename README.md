# Monday — Capture data, label it, and make the computer *detect* signs

Today **you** build the data and teach the computer to recognize traffic signs.
Training the model is one click — the real work (and the real learning) is
collecting good pictures, labelling them, and testing.

You will only edit **one file: `detect.py`** (one or two lines).

---

## The class names — use these EXACT spellings everywhere
```
Stop    Speed25    Speed55    Red    Green    Nothing
```
Folders, Teachable Machine classes — all must match these exactly (capital letters too).

---

## 0) Set up the environment (once)
```bash
Setup anaconda in your machine
```

```bash
conda env create -f environment.yml
conda activate trafficsim
```
*(If that doesn't work: `conda create -n trafficsim python=3.10 -y` → `conda activate trafficsim` → `pip install -r requirements.txt`.)*

---

## 1) Record pictures of the signs
```bash
python monday_app.py
```
A window opens with a car on a road and a cyan **camera box**.

- **Hold the UP ARROW** to drive forward. Signs scroll toward the camera box. Let go to stop.
- When a sign is **inside the camera box**, click **Record** to start saving pictures; click it again to **stop**.
- Drive on, line up the **next** sign, record again. Stopping and restarting Record **keeps** your old pictures (it never overwrites them).
- Also record some **empty road** — those are your `Nothing` pictures.
- Aim for about **30–40 pictures of each sign**. Press **Q** to quit.

All pictures are saved into a folder called **`frames/`**.

> Tip: record each sign at slightly different moments so the pictures vary a little — that makes a stronger model.

---

## 2) Label your pictures (sort them into folders)
This is the important part — **you** decide what each picture is.

1. Open the **`frames/`** folder.
2. Make 6 new folders, named exactly: `Stop`, `Speed25`, `Speed55`, `Red`, `Green`, `Nothing`.
3. Drag each picture into the folder for the sign it shows (empty road → `Nothing`).

---

## 3) Train in Teachable Machine
1. Go to **https://teachablemachine.withgoogle.com** → **Get Started** → **Image Project** → **Standard image model**.
2. Make **6 classes**, named exactly like the folders above.
3. For each class, click **Upload** and drag in the pictures from the matching folder.
4. Click **Train Model**.

## 4) Export the model into this folder
1. **Export Model** → **TensorFlow Lite** tab → **Floating point** → **Download my model**.
2. Unzip it. Put **`model_unquant.tflite`** and **`labels.txt`** in **this** folder (next to `monday_app.py`).

---

## 5) Finish the code — edit `detect.py`
Open **`detect.py`** and complete the two TODOs:

```python
def predict_label(probs, labels):
    # TODO 1: the index of the biggest score
    best =  # <-- write in this line
    # TODO 2 (optional): not sure enough -> "Nothing"
    if Some condition:           # <-- and this line
        return "Nothing"
    return labels[best]
```
- `probs` is the list of scores (one per class); `np.argmax` gives the **position of the biggest** one.
- `labels[best]` is the **name** at that position.

Save the file.

## 6) Watch it detect
```bash
python monday_app.py
```
Now the **Autodetect** button is colored (a model is loaded). Click it, then drive a sign into the camera box — the bottom bar shows what the model thinks it is.

**If it's often wrong:** go back to step 1, record **more and more varied** pictures of the signs it confuses (and more `Nothing`), re-sort, and re-train. This is the real lesson — the model is only as good as the data you give it.

---

## Troubleshooting
- **Autodetect stays gray** → there's no model in the folder yet. Do steps 3–4, then restart the app.
- **It keeps guessing the wrong sign** → not enough / not varied enough training pictures. Record more.
- **`tensorflow` won't install** → make sure you're on **Python 3.10** inside the `trafficsim` env.
- **Wrong camera/window** → not used here (this is a simulator, no webcam needed).
