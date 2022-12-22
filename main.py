import time
import requests
from server import run

if __name__ == '__main__':
    try:
        run()
    except requests.exceptions.ReadTimeout:
        print("Restarting...")
        time.sleep(3)
