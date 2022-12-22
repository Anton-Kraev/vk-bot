import os
from dotenv import load_dotenv
from pyqiwip2p import QiwiP2P

load_dotenv()
p2p = QiwiP2P(auth_key=os.getenv("QIWI_TOKEN"))


def get_status(bill):
    return p2p.check(bill).status


def create_bill(amount):
    return p2p.bill(amount=amount, lifetime=10, comment='')


def reject_bill(bill):
    p2p.reject(bill)


def get_cost(task):
    if task[3] == 'мк':
        if task[2] == 'Тервер и матстат':
            return 150
        return 75
    if task[2] == 'Аналитическая геометрия' and task[3] == 'дз 2.1':
        return 100
    if task[2] == 'Аналитическая геометрия' and task[3] == 'дз 2.2':
        return 75
    if task[2] == 'Аналитическая геометрия' and task[3] == 'кр':
        return 100
    if task[2] == 'Кратинты и ряды' and task[3] == 'дз 2ч1':
        if task[4] in ['Вычисление ротора поля']:
            return 35
        if task[4] in ['Восстановление функции по ее полному дифференциалу с помощью криволинейного интеграла 2-го рода',
                       'Вычисление потока векторного поля по формуле Гаусса-Остроградского',
                       'Независимость криволинейного интеграла 2-го рода от пути интегрирования']:
            return 75
        return 100
    if task[2] == 'Кратинты и ряды' and task[3] == 'дз 2ч2':
        if task[4] in ['Нахождение области сходимости степенного ряда',
                       'Приближенное вычисление определенного интеграла с заданной точностью при помощи степенного ряда']:
            return 75
        return 100
    if task[2] == 'Кратинты и ряды' and task[3] == 'рк1':
        if task[4] == 'теория':
            return 175
        return 75
    if task[2] == 'Кратинты и ряды' and task[3] == 'рк2':
        if task[4] in ['Вычисление ротора градиента скалярного поля',
                       'Вычисление ротора поля']:
            return 35
        if task[4] in ['Вычисление дивергенции векторного поля',
                       'Вычисление циркуляции векторного поля']:
            return 100
        if task[4] in ['Разложение функции в ряд по степеням с использованием известных формул разложений в ряд, определение области сходимости полученного ряда']:
            return 175
        if task[4] == 'теория':
            return 400
        return 150
    if task[2] == 'Кратинты и ряды' and task[3] == 'см 1':
        return 75
    if task[2] == 'Кратинты и ряды' and task[3] == 'см 2':
        if task[4] in ['Найти оценку параметров методом максимального правдоподобия']:
            return 150
        return 100
    return 777
