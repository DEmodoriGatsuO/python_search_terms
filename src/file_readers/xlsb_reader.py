import logging
from typing import Optional
from pyxlsb import open_workbook

def read_xlsb(file_path: str) -> Optional[str]:
    """
    XLSB ファイルを読み込み、その内容を単一の文字列として返します。

    Args:
        file_path (str): 読み込む XLSB ファイルのパス。

    Returns:
        Optional[str]: ファイルの内容を含む文字列。エラーが発生した場合は None を返します。
    """
    try:
        content = []
        with open_workbook(file_path) as wb:
            for sheet_name in wb.sheets:
                with wb.get_sheet(sheet_name) as sheet:
                    for row in sheet.rows():
                        for cell in row:
                            if cell.v is not None:
                                content.append(str(cell.v))
        return ' '.join(content)
    except Exception as e:
        logging.error(f"Error occurred while reading XLSB file {file_path}: {e}")
        return None
