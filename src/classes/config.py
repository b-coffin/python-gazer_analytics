import jmespath
import os

from dotenv import load_dotenv

class Config:

    MODE_GET = "get"
    MODE_REPLACE = "replace"
    
    def __init__(self, config):

        load_dotenv()
        self.host = os.environ.get("LOOKER_HOST")

        self.target_dir: str = jmespath.search("target_dir", config)
        self.mode = jmespath.search("mode", config)
        self.sort_keys= jmespath.search("sort.keys", config)

        if self.mode == "replace":
            self.target_explores = jmespath.search("target_explores", config)
            self.target_views = jmespath.search("target_views", config)
            self.target_fields = jmespath.search("target_fields", config)


    @property
    def host(self):
        return self._host
    
    @host.setter
    def host(self, value):
        if value is None:
            raise ValueError("環境変数 : \"LOOKER_HOST\" が指定されておりません")
        self._host = value


    @property
    def target_dir(self):
        return self._target_dir
    
    @target_dir.setter
    def target_dir(self, value):
        if value is None:
            raise ValueError(f"\"target_dir\" は必須です")
        self._target_dir = value


    @property
    def mode(self):
        return self._mode
    
    @mode.setter
    def mode(self, value):
        mode_list = [self.MODE_GET, self.MODE_REPLACE]
        if value not in mode_list:
            raise ValueError(f"\"mode\" は次のうちのいずれかである必要があります: {', '.join(mode_list)}")
        self._mode = value


