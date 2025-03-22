import json
# import requests
from settings import API_STATUS
from configs.interface import ConfigInterface
from threading import Timer
import os

class Config(ConfigInterface):
    def __init__(self):
        self.data = self.read_config()
        self.observers = []
        self.update_interval = self.parse_interval(self.data["executarEm"])
        self.start_observer()

    def read_config(self):
        print(os.getcwd())
        
        with open(r"src\configs\instructions\config.json", "r") as file:
            data = json.load(file)
        return data

    def parse_interval(self, interval: str):
        unit = interval[-1]
        value = int(interval[:-1])
        
        if unit == "m":
            return value * 60
        elif unit == "h":
            return value * 3600
        else:
            return value

    def get_status_service(self):
        # response = requests.get(API_STATUS, verify=False)
        # data = response.json()
        data = {"status": "ligado"}
        self.data["ativado"] = data.get("status")
        self.notify_observer()
        
    def start_observer(self):
        self.get_status_service()
        Timer(self.update_interval, self.start_observer).start()

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observer(self):
        for observer in self.observers:
            observer.update(self.data)
