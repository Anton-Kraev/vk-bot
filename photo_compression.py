from PIL import Image


def resize(file):
    photo = Image.open(file).convert('RGB')
    w, h = photo.width, photo.height

    # creating full white blank additional(1/2) photo for size 13x8
    if 8 * w > 13 * h:
        blank = Image.new("RGB", (w, round((8 * w - 13 * h) / 26)), (255, 255, 255))
        result = Image.new("RGB", (w, h + blank.height * 2), (255, 255, 255))
        result.paste(blank, (0, 0))
        result.paste(photo, (0, blank.height))
        result.paste(blank, (0, blank.height + h))
    else:
        blank = Image.new("RGB", (round((13 * h - 8 * w) / 16), h), (255, 255, 255))
        result = Image.new("RGB", (w + blank.width * 2, h), (255, 255, 255))
        result.paste(blank, (0, 0))
        result.paste(photo, (blank.width, 0))
        result.paste(blank, (blank.width + w, 0))

    resized_photo = result.resize((390*3, 240*3))
    resized_photo.save(file[:-4] + '-car' + file[-4:])
