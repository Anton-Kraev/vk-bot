import vk_api
from vk_api.upload import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from config import VK_API_TOKEN
import json


session = vk_api.VkApi(token=VK_API_TOKEN)
vk = session.get_api()
longpoll = VkLongPoll(session)
upload = VkUpload(session)

history = {}
with open('paths.json', 'r') as f:
    paths = json.load(f)
with open('photos.json', 'r') as f:
    photos = json.load(f)
