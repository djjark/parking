import os
# from ultralytics import YOLO

if __name__ == '__main__':

    win_path = r"C:\Users\Diogo Cordeiro\OneDrive\Ambiente de Trabalho\Programação\Estacionamentos\datasets\PKLotYoloData\HasXML\UFPR04\Sunny\2012-12-07\2012-12-07_19_32_27.jpg"
    wsl_path = win_path.replace("C:\\", "/mnt/c/").replace("\\", "/")
    print(wsl_path)
    print(os.path.exists(wsl_path))  # Check WSL path


    # # Assuming you've trained a model or loaded a pre-trained model
    # model = YOLO('yolo11n.pt')  # Load a pre-trained model or use your custom training process

    # # Training the model (this is optional if you already have a trained model)
    # model.train(data='./config.yaml', epochs=5, device=0, val=False)

    # # After training or for inference, save the trained model
    # model.save('../model/my_model.pt')


