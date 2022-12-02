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
