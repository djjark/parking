from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
import supervision as sv
from PIL import Image
from ultralytics import YOLO
# Load YOLOv8 model
# model_path = os.path.join(os.path.dirname(__file__), '../../model/my_model.pt')
model_path = os.path.abspath("../../model/my_model.pt")
# Configure upload folder and allowed extensions
UPLOAD_FOLDER = "./uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create Blueprint for the identify-parking route
identify_parking_bp = Blueprint('identify_parking', __name__)

@identify_parking_bp.route('/identify-parking', methods=['POST'])
def identify_parking():
    """Endpoint to process an uploaded image and identify parking spots."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading."}), 400

    # In your route handler:
    if file and allowed_file(file.filename):
    # Save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Load YOLOv8 model
        model = YOLO(model_path)  # or use a custom trained model
                
        # Run inference
        results = model(filepath)
        
        # Process results
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                detection = {
                    "bbox": box.xyxy[0].tolist(),  # Convert tensor to list
                    "confidence": float(box.conf),
                    "class": int(box.cls),
                    "class_name": result.names[int(box.cls)]
                }
                detections.append(detection)

        # Save annotated image
        annotated_image = results[0].plot()
        annotated_image_path = os.path.join(UPLOAD_FOLDER, f"annotated_{filename}")
        Image.fromarray(annotated_image).save(annotated_image_path)

        return jsonify({
            "detections": detections,
            "annotated_image_url": annotated_image_path
        })
    else:
        return jsonify({"error": "File type not allowed."}), 400
