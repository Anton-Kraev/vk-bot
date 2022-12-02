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


def upload_photos(path):
    photos = {}
    print('start uploading photos')
    i = 0
    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            file = dirname.replace('\\', '/') + '/' + filename

            i += 1
            print(i, ' ' + filename)

            if filename[-6:-4] == '-0':
                resized_photo = Image.open(file).resize((390, 240))
                resized_photo.save(file)

            photo = upload.photo_messages(file)[0]
            photos[file] = [str(photo["owner_id"]), str(photo["id"]), str(photo["access_key"])]

    print('uploaded ', i)
    with open('photos.json', 'w') as f:
        json.dump(photos, f)


parse('Начать')
upload_photos('Начать/3 сем/кратинты и ряды/дз2ч1 — копия/Вычисление координат центра масс поверхности с помощью поверхностного интеграла 1-го рода')
