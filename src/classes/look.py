import jmespath


from classes.config import Config

class Look:

    def __init__(self, look_json: dict, config: Config):
        self.json = look_json

        self.folder_id = jmespath.search("folder_id", self.json)
        self.id = self.get_id()
        self.title = self.get_title()
        self.url = self.get_url(config)
        self.explore: str = self.get_explorename()
        self.filters = self.json.get("query.filters", {})


    def get_id(self):
        return jmespath.search('id', self.json)


    def get_title(self):
        return jmespath.search("title", self.json)


    def get_url(self, config: Config):
        return f"https://{config.host}/looks/{self.id}"
    

    def get_explorename(self):
        return jmespath.search("query.view", self.json)
