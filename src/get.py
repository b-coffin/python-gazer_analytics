import json
import os

import util
from classes.config import Config
from classes.dashboard import Dashboard
from classes.look import Look
from classes.query_fields import QueryFields


def gazer_get(input_filenames: list[str], config: Config, input_dir: str, result_dir: str) -> None: # type: ignore
    dbs: list[dict] = []
    for file in input_filenames:
        util.print_with_color(f"### {file}", util.COLOR_BLUE)

        with open(file, "r") as f:
            json_content = json.load(f)

            # シンプルなjsonを作成し、出力
            util.write_dict_to_json(
                os.path.join(result_dir, os.path.basename(file)),
                get_simple_json(json_content, config)
            )

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

    # dbsを、idで並べ替える
    dbs = sorted(dbs, key=lambda x: x["id"]  if x["id"] is not None else "")

    util.write_dicts_to_csv(os.path.join(result_dir, "Dashboards.csv"), dbs)

    return


def get_simple_json(json_content: dict, config: Config) -> dict:
    """
    シンプルなjsonを作成

    Parameters
    ----------
    json_content : dict
        gazerのjsonファイルの中身

    config : Config
        configファイルの内容

    Returns
    -------
    dict
        シンプルなjson
    """


    def get_query_fields(fields: list[QueryFields]) -> list[dict]:
        result = []
        for field in fields:
            result.append({
                "label": field.label,
                "name": field.name,
                "expression": field.expression
            })
        return result
    

    simple_json = {}

    if util.get_json_type(json_content) == util.TYPE_DASHBOARD:
        db = Dashboard(json_content, config)
        simple_json["id"] = db.id
        simple_json["title"] = db.title

        dashboard_elements = []
        for tile in db.tiles:
            dashboard_elements.append({
                "title": tile.title,
                "query": {
                    "view": tile.explore,
                    "fields": tile.fields,
                    "vis_config": {
                        "query_fields": {
                            "table_calculations": sorted(
                                get_query_fields(tile.table_calculations),
                                key=lambda x: x["label"] if x["label"] is not None else ""
                            )
                        }
                    }
                }
            })
        simple_json["dashboard_elements"] = sorted(dashboard_elements, key=lambda x: x["title"] if x["title"] is not None else "")

        dashboard_filters = []
        for filter in db.filters:
            dashboard_filters.append({
                "title": filter.title,
                "default_value": filter.default_value
            })
        simple_json["dashboard_filters"] = sorted(dashboard_filters, key=lambda x: x["title"] if x["title"] is not None else "")

    return simple_json
