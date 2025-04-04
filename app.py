from flask import Flask, request, render_template, jsonify, send_from_directory
import cv2
import numpy as np
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Serve static files
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/outputs/<filename>")
def output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})
    
    # Lưu file vào thư mục uploads
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    return jsonify({"message": "File uploaded successfully", "file_path": f"/uploads/{file.filename}"})

@app.route("/edit", methods=["POST"])
def edit_image():
    data = request.json
    file_path = data.get("file_path")
    action = data.get("action")

    if not file_path or not os.path.exists(file_path.replace("/uploads", UPLOAD_FOLDER)):
        return jsonify({"error": "File not found"})

    image_path = file_path.replace("/uploads", UPLOAD_FOLDER)
    image = cv2.imread(image_path)

    if action == "blur":
        image = cv2.GaussianBlur(image, (15, 15), 0)
    elif action == "grayscale":
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        return jsonify({"error": "Invalid action"})

    # Tạo tên file mới và lưu vào outputs
    output_filename = f"edited_{uuid.uuid4().hex}.jpg"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    cv2.imwrite(output_path, image)

    return jsonify({"message": "Image processed", "output_path": f"/outputs/{output_filename}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

