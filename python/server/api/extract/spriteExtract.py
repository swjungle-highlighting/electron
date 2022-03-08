import os
from PIL import Image
import ffmpeg


CUT_PATH = "./resources/app/storage_dummy"
SC_PATH = "./resources/app/build"
SEC = 10
COL_SPRITE = 60 //SEC
W, H = 177, 100

def make_sprite(input_file) : 
    _clear_dummy()
    output_file = input_file[:len(input_file)-4]
    ffmpeg.input(input_file).output(f"./{CUT_PATH}/{output_file}_%04d.png", r=1/SEC, s=f'{str(W)}x{str(H)}').run()
    _1, _2, files = next(os.walk(CUT_PATH))
    filenum = len(files)
    out_image = Image.new('RGB', (W * COL_SPRITE, H * (filenum //COL_SPRITE + 1)))

    for index, file in enumerate(files) :
        img = Image.open(f"{CUT_PATH}/{file}")
        x = W * (index %COL_SPRITE)
        y = H * (index //COL_SPRITE)
        out_image.paste(img, (x, y))
    out_image.save(f"{SC_PATH}/{output_file}.jpg", quality = 95)

def _clear_dummy() : 
    for file in os.scandir(CUT_PATH) : 
        os.remove(file.path)