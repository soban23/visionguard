import os
from flask import Blueprint, request, render_template, jsonify
from werkzeug.utils import secure_filename
from .inference import predict
from .models import db, Prediction

bp = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 5 * 1024 * 1024
MODEL_VERSION = "champion_v1"

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route("/", methods=["GET"])
def upload_page():
    return render_template("upload.html")

@bp.route("/predict", methods=["POST"])
def predict_route():
    if "image" not in request.files:
        return render_template("error.html", message="No file uploaded."), 400

    file = request.files["image"]

    if file.filename == "":
        return render_template("error.html", message="No file selected."), 400

    if not allowed_file(file.filename):
        return render_template("error.html", message="Unsupported file type. Use PNG or JPG."), 400

    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > MAX_FILE_SIZE:
        return render_template("error.html", message="File too large (max 5MB)."), 400

    filename = secure_filename(file.filename)
    image_bytes = file.read()

    try:
        label, confidence = predict(image_bytes)
    except Exception:
        return render_template("error.html", message="Could not process this file as an image."), 400

    record = Prediction(
        filename=filename,
        label=label,
        confidence=round(confidence, 4),
        model_version=MODEL_VERSION
    )
    db.session.add(record)
    db.session.commit()

    return render_template("result.html", label=label, confidence=round(confidence*100, 2), filename=filename)

@bp.route("/history", methods=["GET"])
def history():
    records = Prediction.query.order_by(Prediction.timestamp.desc()).all()
    return render_template("history.html", records=records)

@bp.route("/health", methods=["GET"])
def health():
    from .inference import load_model
    try:
        load_model()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500
