from configs.config import Config
from manager import Manager

config = Config()
manager = Manager(config)
manager.start()