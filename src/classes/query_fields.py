import jmespath

import util

from classes.config import Config

class QueryFields:

    def __init__(self, json, config: Config):
        self.json = json
        self.label: str = self.get_label()
        self.name: str = self.get_name()
        self.expression: str = self.get_expression()

    def get_label(self) -> str:
        return jmespath.search('label', self.json)


    def get_name(self) -> str:
        return jmespath.search('name', self.json)


    def get_expression(self) -> str:
        return jmespath.search('expression', self.json)
