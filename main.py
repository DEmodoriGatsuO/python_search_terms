from src.file_processor import FileProcessor
from src.utils.config_loader import load_config
from src.utils.logger import setup_logger

def validate_config(config):
    required_keys = ['keywords', 'file_paths', 'notifications', 'logging']
    return all(key in config for key in required_keys)

def main():
    # 設定の読み込みと検証
    config = load_config()
    if not validate_config(config):
        raise ValueError("設定ファイルが不完全です")

    # ロガーのセットアップ
    setup_logger(
        config['logging']['level'],
        config['logging']['format'],
        config['logging']['file_base']
    )

    # FileProcessorのインスタンス化
    processor = FileProcessor(
        config['keywords']['A'],
        config['keywords']['B'],
        config['notifications']['webhook_url'],
        config['notifications']['error_threshold']
    )

    # CSVファイルの処理
    processor.process_csv(config['file_paths']['csv'])

if __name__ == "__main__":
    main()
