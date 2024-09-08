import yaml

def load_config(config_path='config/settings.yaml'):
    # ファイルのエンコーディングをUTF-8に指定して日本語文字列に対応
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)
