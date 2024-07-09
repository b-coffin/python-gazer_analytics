import json
import os
import polars


# Terminal上で必要になるエスケープ処理を入れる
def get_escapedtext_forcommand(text: str) -> str:
    return text.replace(" ", "\\ ").replace("[", "\\[").replace("]", "\\]").replace("(", "\\(").replace(")", "\\)").replace("&", "\\&")


def get_importcommand(arg1, filepath, folder_id, host):
    return f"gzr {arg1} import {get_escapedtext_forcommand(filepath)} {folder_id} --host {host} --force"


TYPE_DASHBOARD = "Dashboard"
TYPE_LOOK = "Look"
TYPR_SPACE = "Space"

def get_json_type(json):
    """
    jsonファイルの内容からDashboard・Look・Spaceを判断

    Parameters
    ----------
    json : dict
        gazerで取得したjsonファイルの内容

    Returns
    -------
    {"Dashboard", "Look", "Space"}
    """
    if "dashboard_elements" in json.keys():
        return TYPE_DASHBOARD
    elif "query" in json.keys():
        return TYPE_LOOK
    else:
        return TYPR_SPACE
    

COLOR_BLUE = "blue"
COLOR_YELLOW = "yellow"
COLOR_GREEN = "green"

def print_with_color(text: str, color: str) -> None:
    if color == COLOR_BLUE:
        print(f"\033[34m{text}\033[0m")
    elif color == COLOR_GREEN:
        print(f"\033[32m{text}\033[0m")
    elif color == COLOR_YELLOW:
        print(f"\033[33m{text}\033[0m")
    else:
        print(text)


# ファイルの書き込み

def write_df_to_csv(path: str, df: polars.DataFrame) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.write_csv(path, separator=",")


def write_dicts_to_csv(path: str, dicts: list[dict]) -> None: # type: ignore
    write_df_to_csv(path, polars.DataFrame(dicts))


def write_dict_to_json(path: str, d: dict) -> None: # type: ignore
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)


def write_text_file(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def append_text_file(path: str, text: str) -> None:
    with open(path, "a") as f:
        f.write(text)
