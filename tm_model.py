"""
tm_model.py  —  load and run a Teachable Machine TensorFlow Lite model.
You do NOT need to edit this file.
"""
import numpy as np


def load_interpreter(path):
    Interpreter = None
    try:
        from tflite_runtime.interpreter import Interpreter
    except ImportError:
        try:
            from ai_edge_litert.interpreter import Interpreter
        except ImportError:
            import tensorflow as tf
            Interpreter = tf.lite.Interpreter      # attribute access, NOT "from tensorflow.lite import"
    interp = Interpreter(model_path=path)
    interp.allocate_tensors()
    return interp


def load_labels(path):
    out = []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        parts = line.split(" ", 1)                 # Teachable Machine format: "0 ClassName"
        out.append(parts[1] if len(parts) > 1 and parts[0].isdigit() else line)
    return out


def input_size(interp):
    _, h, w, _ = interp.get_input_details()[0]["shape"]
    return int(h)


def predict(interp, rgb_array):
    """rgb_array: (H, W, 3) RGB uint8 at the model's input size. Returns a list of probabilities."""
    inp = interp.get_input_details()[0]
    if inp["dtype"] == np.float32:
        data = (rgb_array.astype(np.float32) / 127.5) - 1.0
    else:
        data = rgb_array.astype(np.uint8)
    interp.set_tensor(inp["index"], np.expand_dims(data, 0))
    interp.invoke()
    out = interp.get_output_details()[0]
    probs = interp.get_tensor(out["index"])[0]
    if out["dtype"] != np.float32:
        scale, zero = out["quantization"]
        probs = (probs.astype(np.float32) - zero) * (scale or 1.0)
    total = float(np.sum(probs))
    return probs / total if total > 0 else probs
