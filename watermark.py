import os
import sys

from PIL import Image

EXTS = ('.jpg', '.png')

if len(sys.argv) < 3:
    print('Usage: watermark.py \'image folder path\' \'logo path\' [topleft, topright, bottomleft, bottomright, center]')
    sys.exit()
elif len(sys.argv) == 4:
    path = sys.argv[1]
    lgo = sys.argv[2]
    pos = sys.argv[3]
else:
    path = sys.argv[1]
    lgo = sys.argv[2]

logo = Image.open(lgo)
logo = logo.convert("RGBA")
datas = logo.getdata()
newData = []
for item in datas:
    if (item[0] == 255 and item[1] == 255 and item[2] == 255) or \
            (item[0] == 230 and item[1] == 230 and item[2] == 230):
        newData.append((255, 255, 255, 0))
    else:
        newData.append((item[0], item[1], item[2], 33))
logo.putdata(newData)
logoWidth = logo.width
logoHeight = logo.height

for dirname, _, filenames in os.walk(path):
    for filename in filenames:
        file = dirname.replace('\\', '/') + '/' + filename
        if filename[-6:-4] != '-0':
            image = Image.open(file)
            imageWidth = image.width
            imageHeight = image.height

            try:
                if pos == 'topleft':
                    image.paste(logo, (0, 0), logo)
                elif pos == 'topright':
                    image.paste(logo, (imageWidth - logoWidth, 0), logo)
                elif pos == 'bottomleft':
                    image.paste(logo, (0, imageHeight - logoHeight), logo)
                elif pos == 'bottomright':
                    image.paste(logo, (imageWidth - logoWidth, imageHeight - logoHeight), logo)
                elif pos == 'center':
                    image.paste(logo, ((imageWidth - logoWidth) / 2, (imageHeight - logoHeight) / 2), logo)
                else:
                    print('Error: ' + pos + ' is not a valid position')
                    print(
                        'Usage: watermark.py \'image path\' \'logo path\' [topleft, topright, bottomleft, bottomright, center]')

                image.save(file)
                print('Added watermark to ' + file)

            except:
                image.paste(logo, (int((imageWidth - logoWidth) / 2), int((imageHeight - logoHeight) / 2)), logo)
                image.save(file)
                print('Added default watermark to ' + file)
