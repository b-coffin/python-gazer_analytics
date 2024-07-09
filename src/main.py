import datetime
import glob
import json
import os
import traceback
from zoneinfo import ZoneInfo

from classes.config import Config
from get import gazer_get
from replace import gazer_replace

def main():

    # Configファイルをキーボード入力から取得
    config_file = os.path.join("config", input("Input config file name 1 (default: sample_replace.json) : ") or "sample_replace.json")
    config_json = json.load(open(config_file, "r"))

    # configのバリデーションチェック
    try:
        config = Config(config_json)
    except Exception:
        print(f"Stacktrace: {traceback.format_exc()}")
        return

    # jsonフォルダ配下で、指定したフォルダ配下のファイルをすべて取得
    input_dir: str = os.path.join(os.path.dirname(__file__), "json", config.target_dir)
    input_filenames: list[str] = glob.glob(f"{input_dir}/**/*.json", recursive=True)

    result_dir = os.path.join("result", datetime.datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y%m%d-%H%M%S") + "_" + config.mode)

    if config.mode == config.MODE_GET:
        gazer_get(
            input_filenames=input_filenames,
            config=config,
            input_dir=input_dir,
            result_dir=result_dir,
        )
    elif config.mode == config.MODE_REPLACE:
        gazer_replace(
            input_filenames=input_filenames,
            config=config,
            input_dir=input_dir,
            result_dir=result_dir,
        )

# メイン
if __name__ == "__main__":
    main()
