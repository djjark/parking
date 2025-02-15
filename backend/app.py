import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from werkzeug.utils import secure_filename
from PIL import Image
from ultralytics import YOLO
import numpy as np
import cv2

# Constants
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

app = FastAPI()

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get("/")
def read_root():
    return {"message": "Welcome to the Parking Identification API"}

@app.post("/identify-parking")
async def identify_parking(file: UploadFile = File(...)):
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed.")
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())
    
    # Run YOLO model
    results = model(filepath)
    detections = []
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            detection = {
                "bbox": box.xyxy[0].tolist(),
                "confidence": float(box.conf),
                "class": int(box.cls),
                "class_name": result.names[int(box.cls)]
            }
            detections.append(detection)
    
    # Annotate image
    img = cv2.imread(filepath)
    for detection in detections:
        x1, y1, x2, y2 = map(int, detection["bbox"])
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{detection['class_name']} {detection['confidence']:.2f}"
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    annotated_image_path = os.path.join(UPLOAD_FOLDER, f"annotated_{filename}")
    cv2.imwrite(annotated_image_path, img)
    
    return JSONResponse(content={
        "detections": detections,
        "annotated_image_url": annotated_image_path
    })
# test