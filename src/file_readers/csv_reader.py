import csv
import logging

def read_csv(file_path):
    """
    CSVファイルを読み込み、各行をリストとして返す関数

    Args:
        file_path (str): CSVファイルのパス

    Returns:
        list: CSVの各行をリストとして持つリスト
    """
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            return [row[0] for row in reader if row]  # 各行の最初の要素（ファイルパス）のみを返す
    except Exception as e:
        logging.error(f"Error reading CSV file {file_path}: {e}")
        return []