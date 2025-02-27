import copy
import jmespath
import re

import util

from classes.config import Config
from classes.query_fields import QueryFields

class Tile:

    def __init__(self, tile_json, config: Config):
        self.json = tile_json
        self.id: str = self.get_id()
        self.title: str = self.get_title()
        self.explore: str = self.get_explorename()
        self.explore_url: str = self.get_exploreurl(config)
        self.fields: list[str] = self.get_fields()
        self.measures: list[QueryFields] = self.get_query_fields(config, "measures")
        self.dimensions: list[QueryFields] = self.get_query_fields(config, "dimensions")
        self.table_calculations: list[QueryFields] = self.get_query_fields(config, "table_calculations")


    def get_id(self) -> str:
        return jmespath.search('id', self.json)
    

    def get_explorename(self):
        return jmespath.search("query.view", self.json)


    def get_exploreurl(self, config: Config):
        match: re.Match = re.search(r"(.+)(?:&vis|\?)=", jmespath.search("query.url", self.json) or "")
        if match: 
            return f"https://{config.host}" + match.group(1)
        else:
            return None


    def get_title(self):
        return jmespath.search("title", self.json)


    def get_fields(self) -> list[str]:
        return jmespath.search("query.fields", self.json)
    

    def get_query_fields(self, config: Config, fields_type: str) -> list[QueryFields]:
        result = []
        query_fields = jmespath.search(f"query.vis_config.query_fields.{fields_type}", self.json)
        if type(query_fields) == list:
            for query_field in query_fields:
                result.append(QueryFields(query_field, config))
        return result
