import jmespath

from classes.config import Config
from classes.tile import Tile

from typing import Dict, List

class Dashboard:

    def __init__(self, db_json: dict, config: Config):
        self.json = db_json

        self.folder_id = jmespath.search("folder_id", self.json)
        self.id = jmespath.search('id', self.json)
        self.title = jmespath.search("title", self.json)
        self.url = self.get_url(config)
        self.tiles: List[Tile] = self.get_tiles(config)
        self.filters = self.json.get("dashboard_filters", [])


    def get_id(self):
        return jmespath.search('id', self.json)


    def get_tiles(self, config: Config) -> List[Tile]:
        tiles = []
        for db_elm in self.json.get("dashboard_elements", []):
            tiles.append(Tile(db_elm, config))
        return tiles


    def get_title(self):
        return jmespath.search("title", self.json)


    def get_url(self, config: Config):
        return f"https://{config.host}/{jmespath.search('url', self.json)}"
    