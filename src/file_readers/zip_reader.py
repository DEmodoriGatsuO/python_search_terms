import zipfile
import tempfile
import os
import logging
from .excel_reader import read_excel
from .word_reader import read_word
from .powerpoint_reader import read_powerpoint
from .text_reader import read_text

def read_zip(zip_file_path):
    """
    Zipファイルの内容を読み込み、含まれるファイルを処理する関数

    Args:
        zip_file_path (str): Zipファイルのパス

    Returns:
        dict: ファイル名をキー、抽出されたテキストを値とする辞書
    """
    extracted_contents = {}
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_ref.extractall(temp_dir)
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        content = process_file(file_path)
                        if content:
                            extracted_contents[file] = content
    except Exception as e:
        logging.error(f"Error processing ZIP file {zip_file_path}: {e}")
    return extracted_contents

def process_file(file_path):
    """
    ファイルの種類に応じて適切な読み込み関数を呼び出す

    Args:
        file_path (str): 処理するファイルのパス

    Returns:
        str: 抽出されたテキスト
    """
    if file_path.endswith(('.xlsx', '.xls', '.xlsb')):
        return read_excel(file_path)
    elif file_path.endswith(('.docx', '.doc')):
        return read_word(file_path)
    elif file_path.endswith(('.pptx', '.ppt')):
        return read_powerpoint(file_path)
    elif file_path.endswith('.txt'):
        return read_text(file_path)
    else:
        logging.warning(f"Unsupported file type: {file_path}")
        return None