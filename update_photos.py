import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Web.settings")
import django
django.setup()
from Portfolio.models import Album, Photo
os.system('py C:\\Web\\CollectPhotos.py C:\Web\photo_set C:\Web\static\Portfolio\photos')

FILENAME = 'C:\Web\static\Portfolio\photos\info.json'
with open(FILENAME) as infile:
    info = json.load(infile)

Photo.objects.all().delete()
Album.objects.all().delete()


for album_info in info:
    album = Album(name=album_info['name'], date=album_info['date'], description=album_info['description'])
    album.save()
    for normal_photo, preview_photo in album_info['photos']:
        photo = Photo(big_name=normal_photo, preview_name=preview_photo, album=album)
        photo.save()
