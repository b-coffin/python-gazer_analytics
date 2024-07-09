import json
import os
import re

import util
from classes.config import Config
from classes.dashboard import Dashboard
from classes.look import Look


def gazer_replace(input_filenames: list[str], config: Config, input_dir: str, result_dir: str) -> None: # type: ignore
    result_gzrcommand = ""
    result_revertcommand = ""

    for file in input_filenames:
        util.print_with_color(f"### {file}", util.COLOR_BLUE)

        with open(file, "r") as f:
            json_content: dict = json.load(f)
            new_json_content: dict = get_replaced_json(json_content, config)

            if new_json_content and new_json_content != json_content:
                result_json_path = os.path.join(result_dir, os.path.relpath(file, input_dir))

                util.write_dict_to_json(result_json_path, new_json_content)

                if util.get_json_type(json_content) == util.TYPE_DASHBOARD:
                    db = Dashboard(json_content, config)
                    result_gzrcommand += util.get_importcommand("dashboard", result_json_path, db.id, config.host) + "\n"
                    result_revertcommand += util.get_importcommand("dashboard", os.path.relpath(file, os.path.dirname(__file__)), db.id, config.host) + "\n"
                elif util.get_json_type(json_content) == util.TYPE_LOOK:
                    look = Look(json_content, config)
                    result_gzrcommand += util.get_importcommand("look", result_json_path, look.id, config.host) + "\n"
                    result_revertcommand += util.get_importcommand("look", os.path.relpath(file, os.path.dirname(__file__)), look.id, config.host) + "\n"

    util.write_text_file(os.path.join(result_dir, "gzr.sh"), result_gzrcommand)
    util.write_text_file(os.path.join(result_dir, "revert.sh"), result_revertcommand)

    return


def get_replaced_json(json_content: dict, config: Config) -> dict:
    """
    指定したオブジェクトを置換したjsonを返す

    Parameters
    ----------
    json_content : dict
        gazerのjsonファイルの中身

    config : Config
        configファイルの内容

    Returns
    -------
    dict
        置換後のjson
    """
    result = json.dumps(json_content)

    # explore名を置換
    if config.target_explores and type(config.target_explores) == list:
      for e in config.target_explores:
          result = re.sub(fr"(\"){e['before']}(\"\,\s*\"(?:dimension|fields|name|suggestable)\")", fr"\1{e['after']}\2", result)
          result = re.sub(fr"(/){e['before']}(\?)", fr"\1{e['after']}\2", result)

    # view名を置換
    for v in config.target_views:
        result = re.sub(fr"(\"){v['before']}(\.)", fr"\1{v['after']}\2", result)
        result = re.sub(fr"(\"){v['before']}(\"\,\s*\"(?:dimension_group|suggest_dimension|view_label)\")", fr"\1{v['after']}\2", result)
        result = re.sub(fr"(\,){v['before']}(\.)", fr"\1{v['after']}\2", result)
        result = re.sub(fr"(\[){v['before']}(\.)", fr"\1{v['after']}\2", result)
        result = re.sub(fr"(=){v['before']}(\.)", fr"\1{v['after']}\2", result)
        result = re.sub(fr"(/){v['before']}(\.view\.lkml)", fr"\1{v['after']}\2", result)
        result = re.sub(fr"(\$\{{){v['before']}(\.)", fr"\1{v['after']}\2", result)
        result = re.sub(fr"((?:show_comparison|show_title|style|title_override|title_placement|value_format)_){v['before']}(\.)", fr"\1{v['after']}\2", result)

    # field名を置換
    if config.target_fields and type(config.target_fields) == list:
        for f in config.target_fields:
            result = re.sub(fr"(\"){f['before']}(\"(?:,|\s*\]|:))", fr"\1{f['after']}\2", result)
            result = re.sub(fr"(,){f['before']}((?:,|&))", fr"\1{f['after']}\2", result)

    return json.loads(result)
