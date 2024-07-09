import json
import os

import util
from classes.config import Config
from classes.dashboard import Dashboard
from classes.look import Look


def gazer_get(input_filenames: list[str], config: Config, input_dir: str, result_dir: str) -> None: # type: ignore
    dbs: list[dict] = []
    for file in input_filenames:
        util.print_with_color(f"### {file}", util.COLOR_BLUE)

        with open(file, "r") as f:
            json_content = json.load(f)

            if util.get_json_type(json_content) == util.TYPE_DASHBOARD:
                db = Dashboard(json_content, config)
                for tile in db.tiles:
                    dbs.append({
                        "type": util.TYPE_DASHBOARD,
                        "id": db.id,
                        "title": db.title,
                        "URL": db.url,
                        "folder": os.path.dirname(os.path.relpath(file, input_dir)),
                        "tile": tile.title,
                        "explore": tile.explore
                    })
            elif util.get_json_type(json_content) == util.TYPE_LOOK:
                look = Look(json_content, config)
                dbs.append({
                    "type": util.TYPE_LOOK,
                    "id": look.id,
                    "title": look.title,
                    "URL": look.url,
                    "folder": os.path.dirname(os.path.relpath(file, input_dir)),
                    "tile": None,
                    "explore": look.explore
                })

    util.write_dicts_to_csv(os.path.join(result_dir, "Dashboards.csv"), dbs)

    return
