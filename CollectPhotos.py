from PIL import Image
import os
import sys
import json

ALBUM_FILE = 'description.txt'
IMAGES_EXTS = ['.jpg', '.jpeg', '.png', '.JPG']
# PREVIEW_SIZE = (300, 225)
PREVIEW_SIZE = (200, 150)
NORMAL_SIZE = (2000, 1500)

def print_usage():
    print('Usage: {} input_dir output_dir'.format(sys.argv[0]))
    exit(-1)

try:
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
except:
    print_usage()

obj = []

for dirpath, dirnames, filenames in os.walk(input_dir):
    if ALBUM_FILE in filenames:
        with open(os.path.join(dirpath, ALBUM_FILE)) as desc_file:
            album_name = desc_file.readline()
            album_date = desc_file.readline()
            album_desc = desc_file.read()
        album = {
            'name': album_name,
            'date': album_date,
            'description': album_desc,
            'photos': []
        }
        for image_name in filenames:
            if image_name == ALBUM_FILE:
                continue
            _, ext = os.path.splitext(image_name)
            if ext not in IMAGES_EXTS:
                continue
            normal_image = Image.open(os.path.join(dirpath, image_name))
            normal_image.thumbnail(NORMAL_SIZE)
            preview_image = normal_image.copy()
            preview_image.thumbnail(PREVIEW_SIZE)
            normal_image.save(os.path.join(output_dir, image_name))
            preview_image.save(os.path.join(output_dir, 'preview' + image_name))
            album['photos'].append((image_name, 'preview' + image_name))
        obj.append(album)
info_name = os.path.join(output_dir, 'info.json')
with open(info_name, 'w') as outfile:
    json.dump(obj, outfile)

