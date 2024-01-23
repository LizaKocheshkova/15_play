from PIL import Image
import random
import os

def load_img_lvl():
    img = Image.open(f'images/lvl/{random.choice(os.listdir("images/lvl"))}')
    img = img.resize((520, 520))
    for i in range(4):
        for j in range(4):
            temp = img.crop((i * 130, j * 130, i * 130 + 129, j * 130 + 129))
            temp.save(f'images/temp/{i + j * 4}.jpg')


if __name__ == "__main__":
    print(os.listdir('images/lvl'))