import os
import io
import json
import base64
from PIL import Image, ImageDraw, ImageFont
# from io import BytesIO

BASE_DIR = '.'
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SRC_DIR = './src'
SRC_DIR = os.path.join(BASE_DIR, 'src')

# STICKERS_DIR = './static'
STICKERS_DIR = os.path.join(BASE_DIR, 'static')

# TST_DIR = './tst'
TST_DIR = os.path.join(BASE_DIR, 'tst')

SUPPORTED_FILES = ['png']

AUTHOR = 'Guga'
PACK_NAME = 'By @FlorkOfCows'

def get_supported_files(directory):
    only_files = [item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))]
    return [file_item for file_item in only_files if file_item.split('.')[1].lower() in SUPPORTED_FILES]

def main():
    fnt = ImageFont.truetype(os.path.join(SRC_DIR, 'comic.ttf'), 130)
    base = Image.open(os.path.join(SRC_DIR, 'base_pokeball.png')).convert('RGBA')
    base_w, base_h = base.size
    txt = Image.new('RGBA', base.size, (255,255,255,0))
    d = ImageDraw.Draw(txt)
    
    num = '0032'
    fim = '028_A'.replace('_',' ')
        
    txti_w, txti_h = d.textsize(num, font=fnt)
    txtf_w, txtf_h = d.textsize(fim, font=fnt)
    
    d.text(( (base_w - txti_w)/2 , 10 ), num, font=fnt, fill='white')
    d.text(( (base_w - txtf_w)/2 , base_h - txtf_h - 60 ), fim, font=fnt, fill='black')
    
    out = Image.alpha_composite(base, txt)
    
    out.show()
    # out.save(os.path.join(BASE_DIR, 'teste.png'), 'PNG')

'''
    with open("yourfile.ext", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    buffered = io.BytesIO()
    out.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    del buffered
    print(img_str)

    with open('data.json', 'w') as fp:
    json.dump(data, fp)
'''

if __name__ == '__main__':
    main()