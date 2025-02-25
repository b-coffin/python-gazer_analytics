import jmespath

import util

from classes.config import Config

class Filter:

    def __init__(self, filter_json, config: Config):
        self.json = filter_json
        self.id: str = self.get_id()
        self.title: str = self.get_title()
        self.default_value: str = self.get_default_value()


    def get_id(self) -> str:
        return jmespath.search('id', self.json)
    

    def get_title(self):
        return jmespath.search("title", self.json)


    def get_default_value(self):
        return jmespath.search("default_value", self.json)