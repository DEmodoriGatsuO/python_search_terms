import logging

def read_text(file_path):
    """
    テキストファイルの内容を読み込む関数

    Args:
        file_path (str): テキストファイルのパス

    Returns:
        str: ファイルの内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error reading text file {file_path}: {e}")
        return ""