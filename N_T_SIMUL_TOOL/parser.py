import textfsm
import pandas as pd
from pathlib import Path

def parse_config_file(file_path, template_path):
    with open(template_path) as tpl, open(file_path) as cfg:
        fsm = textfsm.TextFSM(tpl)
        parsed = fsm.ParseText(cfg.read())
        df = pd.DataFrame(parsed, columns=fsm.header)
        df["DEVICE"] = Path(file_path).stem
        return df

def parse_all_configs(config_folder, template_path):
    all_dfs = []
    for file in Path(config_folder).glob("*.txt"):
        df = parse_config_file(file, template_path)
        all_dfs.append(df)
    return pd.concat(all_dfs, ignore_index=True)
