import json
import os
from dict import push
from PIL import Image
from vk import upload


def parse(path):
    paths_dict = {'Начать': {}}

    for dirname, dirnames, filenames in os.walk(path):
        if dirnames:
            push(paths_dict, dirname.split('\\')[:-1], dirname.split('\\')[-1], {})

        for subdirname in dirnames:
            push(paths_dict, dirname.split('\\'), subdirname, [])

        for filename in filenames:
            push(paths_dict, dirname.split('\\'), '', filename)

    with open('paths.json', 'w') as f:
        json.dump(paths_dict, f)


with open('photos.json', 'r') as f:
    photos = json.load(f)


def upload_photos(path):
    print('start uploading photos')
    i = len(photos)

    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            file = dirname.replace('\\', '/') + '/' + filename

            if filename[-6:-4] == '-0':
                resized_photo = Image.open(file).resize((390, 240))
                resized_photo.save(file)

            if file in photos.keys():
                continue

            i += 1
            print(i, ' ' + filename)

            photo = upload.photo_messages(file)[0]
            photos[file] = [str(photo["owner_id"]), str(photo["id"]), str(photo["access_key"])]

    with open('photos.json', 'w') as f:
        json.dump(photos, f)
    print('uploaded ', i)


parse('Начать')
try:
    upload_photos('Начать')
except:
    with open('photos.json', 'w') as f:
        json.dump(photos, f)
