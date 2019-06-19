import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = '.'
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SRC_DIR = './src'
SRC_DIR = os.path.join(BASE_DIR, 'src')

# STICKERS_DIR = './static'
STICKERS_DIR = os.path.join(BASE_DIR, 'static')

# TST_DIR = './tst'
TST_DIR = os.path.join(BASE_DIR, 'tst')


fnt = ImageFont.truetype(os.path.join(SRC_DIR, 'comic.ttf'), 130)

num = '001'
fim = '028 A'

base = Image.open(os.path.join(SRC_DIR, 'base_pokeball.png')).convert('RGBA')
base_w, base_h = base.size

txt = Image.new('RGBA', base.size, (255,255,255,0))
d = ImageDraw.Draw(txt)

txti_w, txti_h = d.textsize(num, font=fnt)
txtf_w, txtf_h = d.textsize(fim, font=fnt)

d.text(( (base_w - txti_w)/2 , 10 ), num, font=fnt, fill='white')
d.text(( (base_w - txtf_w)/2 , base_h - txtf_h - 60 ), fim, font=fnt, fill='black')

out = Image.alpha_composite(base, txt)

out.show()
# out.save(os.path.join(BASE_DIR, 'teste.png'), 'PNG')