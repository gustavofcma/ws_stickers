import os
import io
import json
import base64
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = '.'
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SRC_DIR = os.path.join(BASE_DIR, 'src')
STICKERS_DIR = os.path.join(BASE_DIR, 'static')
TST_DIR = os.path.join(BASE_DIR, 'tst')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

SUPPORTED_FILES = ['webp']

PACK_SIZE = 30
AUTHOR = 'Guga'
PACK_NAME = 'By @FlorkOfCows'
ID_PREFIX = '5521-Florks'

def get_supported_files(directory):
    only_files = [item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))]
    return [file_item for file_item in only_files if file_item.split('.')[1].lower() in SUPPORTED_FILES]

def create_sliced_list_of_lists(original_list, slice_size):
    output_list = []
    for index in range(0, len(original_list), slice_size):
        if len(original_list) - index < slice_size:
            output_list.append(original_list[index:index + (len(original_list) - slice_size)])
        else:
            output_list.append(original_list[index:index + slice_size])
    return output_list

def encode_images_to_base64(image_list):
    encoded_images = []
    for image_file in image_list:
        sticker_data = {}

        with open(os.path.join(STICKERS_DIR, image_file), 'rb') as fl:
            encoded_string = base64.b64encode(fl.read())
        sticker_data['image_data'] = encoded_string.decode('utf-8')
        sticker_data['emojis'] = []

        encoded_images.append(sticker_data)

    return encoded_images

def main():
    fnt = ImageFont.truetype(os.path.join(SRC_DIR, 'comic.ttf'), 130)
    base = Image.open(os.path.join(SRC_DIR, 'base_pokeball.png')).convert('RGBA')
    base_w, base_h = base.size

    arqs = get_supported_files(STICKERS_DIR)
    
    # for i, x in enumerate(create_sliced_list_of_lists(arqs, PACK_SIZE)):
    #     print(f'Pack {i+1}:\nInicio: {x[0].split(".")[0].replace("_0","").replace("_"," ")}\nTermino: {x[-1].split(".")[0].replace("_0","").replace("_"," ")}\n{x}\n')

    packs_list = create_sliced_list_of_lists(arqs, PACK_SIZE)

    for pack in packs_list:
        pack_dict = {}

        first_item = pack[0].split('.')[0]
        first_sticker = first_item.replace('_0', '').replace('_', ' ')
        last_item = pack[-1].split('.')[0]
        last_sticker = last_item.replace('_0', '').replace('_', ' ')

        pack_dict['publisher'] = AUTHOR
        pack_dict['name'] = f'{first_sticker} - {last_sticker} {PACK_NAME}'
        pack_dict['identifier'] = f'{ID_PREFIX}-{first_item}-{last_item}'

        txt = Image.new('RGBA', base.size, (255,255,255,0))
        d = ImageDraw.Draw(txt)

        first_w, first_h = d.textsize(first_sticker, font=fnt)
        last_w, last_h = d.textsize(last_sticker, font=fnt)

        d.text(( (base_w - first_w)/2 , 8 ), first_sticker, font=fnt, fill='white')
        d.text(( (base_w - last_w)/2 , base_h - last_h - 50 ), last_sticker, font=fnt, fill='black')

        out = Image.alpha_composite(base, txt)

        buffered = io.BytesIO()
        out = out.resize((96,96),Image.ANTIALIAS)
        out.save(buffered, format="WEBP", optimize=True, quality=95)
        # out.save(os.path.join(OUTPUT_DIR, f'{first_item}.png'), 'PNG')
        img_str = base64.b64encode(buffered.getvalue())
        del buffered

        pack_dict['tray_image'] = img_str.decode('utf-8')

        sticker_list = encode_images_to_base64(pack)
        pack_dict['stickers'] = sticker_list

        with open(os.path.join(OUTPUT_DIR, f'{ID_PREFIX}-{first_item}-{last_item}.json'), 'w') as fp:
            json.dump(pack_dict, fp)

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
