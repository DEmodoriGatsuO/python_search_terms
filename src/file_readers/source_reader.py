import pandas as pd
import unicodedata

def read_excel(excel_file):
    """
    Excelファイルからファイルパスのリストを取得します。
    """
    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
        if 'FilePath' not in df.columns:
            raise ValueError("'FilePath' 列が存在しません。")
        
        # 'FilePath' 列を正規化してリストとして返す
        file_paths = df['FilePath'].dropna().apply(lambda x: unicodedata.normalize('NFC', str(x))).tolist()
        return file_paths
    except Exception as e:
        logging.getLogger(__name__).error(f"Excelファイルの読み込み中にエラーが発生しました ({excel_file}): {e}")
        return []
