import os
from glob import glob
import random

YoloFolder = os.path.abspath("../datasets")+"/PKLotYoloData/"
SubDirs = ["UFPR04/Sunny/", "UFPR04/Rainy/", "UFPR04/Cloudy/", "UFPR05/Sunny/", "UFPR05/Rainy/", "UFPR05/Cloudy/", "PUCPR/Sunny/","PUCPR/Rainy/", "PUCPR/Cloudy/"]
train_txt = os.path.abspath("../datasets")+"/working/train.txt"
val_txt = os.path.abspath("../datasets")+"/working/val.txt"

if __name__ == '__main__':

    percentage_train = 90

    data_list = {
        "train": [],
        "valid": []
    }

    def appendData(_images, type):
        for img in _images:
            data_list[type].append(img)

    for _folder in SubDirs:
        folder = YoloFolder + "HasXML/" + _folder
        dir_content = [d for d in os.listdir(os.path.join(YoloFolder,folder)) if os.path.isdir(os.path.join(YoloFolder,folder,d))]
        for d in dir_content:
            folder_path = os.path.join(YoloFolder,folder,d)
            images = glob(os.path.join(folder_path, "*.jpg"))
            random.shuffle(images)
            total = len(images)
            train_data_amount = round(total / 100 * percentage_train)
            train_data = images[:train_data_amount]
            appendData(train_data, "train")
            if len(train_data) < total:
                val_data = images[train_data_amount:]
                appendData(val_data, "valid")

    with open(train_txt, 'w') as outfile:
        outfile.write("\n".join(data_list["train"]))
    with open(val_txt, 'w') as outfile:
        outfile.write("\n".join(data_list["valid"]))