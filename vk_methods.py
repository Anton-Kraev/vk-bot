import os
import json
from PIL import Image
from vk import VkKeyboard, VkKeyboardColor, vk, session, upload, get_random_id, history, photos


def get_full_path(history, img):
    return '/'.join(history) + f'/{img}'


def create_keyboard(buttons):
    keyboard = VkKeyboard(one_time=False)

    if not buttons:
        keyboard.add_button(label='Начать', color=VkKeyboardColor.SECONDARY)
    for button in buttons:
        keyboard.add_button(label=button, color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()


def send_message(user_id, message):
    session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id()})


def send_keyboard(user_id, message, keyboard):
    session.method('messages.send',
                   {'user_id': user_id, 'message': message, 'random_id': get_random_id(),
                    'keyboard': keyboard})


def send_carousel(user_id, message, url='', title='', description=''):
    if not url and not (title and description):
        return

    carousel = {
        "type": "carousel",
        "elements": [{
            "buttons": [{
                "action": {
                    "type": "open_link",
                    "label": "Оплатить",
                    "link": history[user_id]['bill'].pay_url
                }
            }]
        }]
    }

    if url:
        photo = photos[url]
        carousel["elements"][0]["photo_id"] = f'{photo["owner_id"]}_{photo["id"]}'
        carousel["elements"][0]["action"] = {"type": "open_photo"}
    if title and description:
        carousel["elements"][0]["title"] = title
        carousel["elements"][0]["description"] = description

    vk.messages.send(user_id=user_id, message=message, random_id=get_random_id(),
                     template=str(json.dumps(carousel, ensure_ascii=False).encode('utf-8').decode('utf-8')))


def send_photo(user_id, message, url):
    photo = photos[url]
    attachment = f'photo{photo["owner_id"]}_{photo["id"]}_{photo["access_key"]}'
    vk.messages.send(user_id=user_id, message=message, random_id=get_random_id(), attachment=attachment)
