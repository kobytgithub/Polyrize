import json
from utils.singleton import Singleton
from config.configuration import Conf


class ScenarioParser(object, metaclass=Singleton):

    data = None
    loaded = False
    scenario_path = ""

    def __init__(self):
        super(ScenarioParser, self).__init__()
        conf = Conf("general")
        self.scenario_path = conf.get_string("scenario")
        self.__load()

    def __load(self):
        with open(self.scenario_path) as f:
            self.data = json.load(f)
        self.loaded = True

    def get_test_list(self):
        return self.data['scenario']

    def get_settings(self):
        if 'settings' in self.data:
            return self.data['settings']
        else:
            return None
