import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
from dotenv import load_dotenv
load_dotenv()

IMG_SIZE = 224
MODEL_PATH = os.environ.get("MODEL_PATH", "model/champion_model.keras")
CLASS_NAMES = ["AiArtData", "RealArt"] 
_model = None

def load_model():
    global _model
    if _model is None:
        _model = tf.keras.models.load_model(MODEL_PATH)
    return _model

def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))
    arr = np.array(img, dtype=np.float32)
    arr = tf.keras.applications.mobilenet_v2.preprocess_input(arr)  
    arr = np.expand_dims(arr, axis=0)
    return arr

def predict(image_bytes):
    model = load_model()
    arr = preprocess_image(image_bytes)
    prob = float(model.predict(arr, verbose=0)[0][0])
    label = CLASS_NAMES[int(prob > 0.5)]
    confidence = prob if label == "RealArt" else 1 - prob
    return label, confidence
