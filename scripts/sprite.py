import os
from PIL import Image
import ffmpeg


SC_PATH = "./"
SEC = 10
COL_SPRITE = 60 //SEC
W, H = 177, 100

def make_sprite(input_file, output_file) :
    ffmpeg.input(input_file).output(f"{SC_PATH}/{output_file}_%04d.png", r=1/SEC, s=f'{str(W)}x{str(H)}').run()
    _1, _2, files = next(os.walk(SC_PATH))
    filenum = len(files)
    out_image = Image.new('RGB', (W * COL_SPRITE, H * (filenum //COL_SPRITE + 1)))

    for index, file in enumerate(files) :
        img = Image.open(f"{SC_PATH}/{file}")
        x = W * (index %COL_SPRITE)
        y = H * (index //COL_SPRITE)
        out_image.paste(img, (x, y))
    out_image.save(f"{SC_PATH}/{output_file}", quality = 95)


make_sprite('gdZLi9oWNZg.mp4', 'test.jpg')
print('succ')