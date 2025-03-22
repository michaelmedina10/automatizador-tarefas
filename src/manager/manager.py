import importlib
from threading import Timer

from configs.interface import ConfigInterface

class Manager:
    def __init__(self, config: ConfigInterface):
        self.config = config
        self.config.register_observer(self)
        self.coletores = {}
 
    def start(self):
        self.setup_coletores()
       
    def update(self, new_config):
        self.reconfigure_config(new_config)

    def setup_coletores(self):
        for coletor_config in self.config.data["coletores"]:
            nome = coletor_config["nome"]
            intervalo = self.config.parse_interval(coletor_config["intervalo"])
            self.instanciar_coletor(nome, coletor_config)
            self.schedule_coletor(nome, intervalo)

    def reconfigure_config(self, new_config):
        for coletor_config in new_config["coletores"]:
            nome = coletor_config["nome"]
            intervalo = self.config.parse_interval(coletor_config["intervalo"])
            if nome in self.coletores:
                self.schedule_coletor(nome, intervalo)
            else:
                self.instanciar_coletor(nome, coletor_config)
                self.schedule_coletor(nome, intervalo)

    def instanciar_coletor(self, nome: str, config: dict):
        modulo = importlib.import_module(f"collectors.{nome}.{nome}")
        class_collector = getattr(modulo, nome.capitalize())
        self.coletores[nome] = class_collector(config)

    def schedule_coletor(self, nome: str, intervalo: str):
        Timer(intervalo, self.execute_coletor, [nome]).start()

    def execute_coletor(self, nome):
        coletor = self.coletores[nome]
        try:
            coletor.executar()
        except Exception as e:
            print(f"Erro ao executar {nome}: {e}")
        finally:
            intervalo = self.config.parse_interval(coletor.config["intervalo"])
            self.schedule_coletor(nome, intervalo)

