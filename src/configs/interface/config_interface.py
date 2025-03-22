from abc import ABC, abstractmethod

class ConfigInterface(ABC):

    @abstractmethod
    def read_config(self):
        ...

    @abstractmethod
    def parse_interval(self, interval: str):
        ...

    @abstractmethod
    def get_status_service(self):
        ...
        
    @abstractmethod
    def start_observer(self):
        ...

    @abstractmethod
    def register_observer(self, observer):
        ...

    @abstractmethod
    def notify_observer(self):
        ...