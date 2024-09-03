import os
import random
from threading import Thread
from time import sleep
import requests


URL_BASE = f"http://{os.environ['BE_HOST_NAME']}:{os.environ['BE_HOST_PORT']}"
URL_SENSOR = "/sensor"
URL_DATA = "/data"
NUM_TH = random.randint(1, 2)
NUM_DATA = random.randint(3, 7)
DATA_TYPE = ["temp", "press"]


def th_method(id: int, data_type: str):
    url = URL_BASE + URL_SENSOR

    payload = {"_id": random.randint(1, 30), "data_type": data_type}
    res = requests.post(url, json=payload)
    
    payload = {"_id": 1, "data_type": data_type} # inject errors
    
    if not random.randint(0,10):
        sleep(random.randint(1, 15))
        requests.post(url, json=payload)

    if res.status_code == 201:
        
        url = URL_BASE + URL_DATA
        for _ in range(NUM_DATA):
            sleep(random.randint(10, 40))

            payload = {"sensor_id": id, "data": random.randint(1, 50)}
            requests.post(url, params={"data_type": data_type}, json=payload)
        
        if not random.randint(0,7):
            requests.post(url, params={"data_type": "wrong"}, json=payload)
        


if __name__ == "__main__":

    th = []

    for i in range(NUM_TH):
        sleep(random.randint(10, 50))

        data_type = "temp" if random.randint(0,1) else "press"
        th.append(Thread(name="sensor_th", target=th_method, args=((i+1), data_type), daemon=True))
        th[i].start()

    for i in range(NUM_TH):
        th[i].join()