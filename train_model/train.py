import os
from ultralytics import YOLO

if __name__ == '__main__':

  
    # Assuming you've trained a model or loaded a pre-trained model
    model = YOLO('yolo11n.pt')  # Load a pre-trained model or use your custom training process

    # Training the model (this is optional if you already have a trained model)
    model.train(data='./config.yaml', epochs=5, batch=8, device=0)

    # After training or for inference, save the trained model
    model.save('../backend/model/my_model.pt')


