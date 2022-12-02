from dict import find
from vk import longpoll, VkEventType, history, paths
from vk_methods import send_message, send_photo, send_carousel, create_keyboard, send_keyboard, get_full_path
from payment import create_bill, get_status, reject_bill


def run():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text
                user_id = event.user_id

                if message == 'Отмена' and history.get(user_id) and \
                        (len(history[user_id]['current']) == 6 or
                         (len(history[user_id]['current']) == 5 and history[user_id]['current'][-2] == 'мк')):
                    history[user_id]['current'] = history[user_id]['current'][:-1]
                    reject_bill(history[user_id]['bill'])
                    history[user_id]['bill'] = None

                if message == 'Проверить оплату' and history.get(user_id):
                    bill = history[user_id]['bill']
                    if not bill or get_status(bill) == 'REJECTED' or get_status(bill) == 'EXPIRED':
                        send_message(user_id, 'Нет активных счетов к оплате')
                        if bill:
                            history[user_id]['current'] = history[user_id]['current'][:-1]
                            history[user_id]['bill'] = None
                    elif get_status(bill) == 'PAID':
                        current = history[user_id]['current']
                        if len(current) == 6:
                            answers = [el for el in find(paths, current[:-1]) if
                                       (el[:-5] == current[-1][:-5] and el[-5] != '0') or (el[:-4] == current[-1][:-6])]
                            # логика обработки нескольких фотографий с ответами
                            for ans in answers:
                                send_photo(user_id, '*', get_full_path(current[:-1], ans))
                        elif len(current) == 5 and current[-2] == 'мк':
                            for i, photo in enumerate(find(paths, current)):
                                send_photo(user_id, str(i + 1), get_full_path(current, photo))
                        history[user_id] = {'current': ['Начать'], 'bill': None}
                        continue
                    else:
                        send_message(user_id, 'Счет не оплачен, либо запрос обрабатывается. '
                                              'Попробуйте повторить команду через '
                                              'пару минут.\nПри возникновении проблем с оплатой '
                                              'можно обратиться к администратору сообщества')
                        continue

                if user_id not in history.keys() or not history[user_id]:
                    history[user_id] = {'current': ['Начать'], 'bill': None}
                    #тут отправить инструкцию
                    #send_message(user_id, '')
                elif message != 'Проверить оплату' and message != 'Отмена':
                    current = history[user_id]['current']
                    if len(current) < 5:
                        variants = find(paths, current)
                    else:
                        variants = [el for el in find(paths, current) if el[-6:-4] == '-0']

                    if message == 'Начать заново' and not history[user_id]['bill']:
                        if len(current) > 1:
                            history[user_id]['current'] = current[:1]
                    elif message == 'Назад' and not history[user_id]['bill']:
                        if len(current) > 1:
                            history[user_id]['current'] = current[:-1]
                    elif message.isdigit() and int(message) in range(1, len(variants) + 1):
                        history[user_id]['current'].append(variants[int(message) - 1])
                    else:
                        send_message(user_id, 'Неизвестная команда')
                        continue

                current = history[user_id]['current']
                if len(current) == 1:
                    send_message(user_id, 'Выберите семестр:')
                if len(current) == 2:
                    send_keyboard(user_id, 'Выберите предмет:', create_keyboard(['Назад', 'Начать заново']))
                if len(current) == 3:
                    send_keyboard(user_id, 'Выберите работу:', create_keyboard(['Назад', 'Начать заново']))
                if len(current) == 4:
                    if current[-1] == 'мк':
                        send_keyboard(user_id, 'Выберите вариант:', create_keyboard(['Назад', 'Начать заново']))
                    else:
                        send_keyboard(user_id, 'Выберите тему:', create_keyboard(['Назад', 'Начать заново']))
                if len(current) == 5:
                    if current[-2] == 'мк':
                        history[user_id]['bill'] = create_bill(1)
                        send_carousel(user_id, 'Выбранная работа\n',
                                      title='мк', description=f'мк вариант {current[-1][-1]}')
                        send_keyboard(user_id, 'Чтобы получить ответы на выбранный вариант, оплатите его по ссылке(qiwi)'
                                               ', нажав на кнопку "оплатить", а затем нажмите на кнопку "Проверить оплату".'
                                               'Чтобы вернуться к выбору заданий, нажмите на кнопку "Отмена"(не следует '
                                               'нажимать на кнопку "Отмена", если вы оплатили задание, но еще не получили'
                                               ' ответ, так как это может привести к утере оплаты)',
                                      create_keyboard(['Проверить оплату', 'Отмена']))
                    else:
                        send_keyboard(user_id,
                                      'Найдите свое задание в списке(будьте внимательны, задания могут быть очень похожи):',
                                      create_keyboard(['Назад', 'Начать заново']))
                if len(current) == 6:
                    history[user_id]['bill'] = create_bill(1)
                    send_carousel(user_id, 'Выбранное задание\n',
                                  url=get_full_path(current[:-1], current[-1]))
                    send_keyboard(user_id, 'Чтобы получить ответ на выбранное задание, оплатите его по ссылке(qiwi)'
                                           ', нажав на кнопку "оплатить", а затем нажмите на кнопку "Проверить оплату".'
                                           'Чтобы вернуться к выбору заданий, нажмите на кнопку "Отмена"(не следует '
                                           'нажимать на кнопку "Отмена", если вы оплатили задание, но еще не получили'
                                           ' ответ, так как это может привести к утере оплаты)',
                                  create_keyboard(['Проверить оплату', 'Отмена']))

                variants = find(paths, current)
                if len(current) < 5:
                    choose_variant = '\n'.join([f'{i + 1} - {el}' for i, el in enumerate(variants)])
                    send_message(user_id, choose_variant)
                elif len(current) == 5 and current[-2] != 'мк':
                    for i, photo in enumerate([el for el in variants if el[-6:-4] == '-0']):
                        send_photo(user_id, str(i + 1), get_full_path(current, photo))
