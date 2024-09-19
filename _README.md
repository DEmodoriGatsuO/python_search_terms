# File Processing Script Documentation

## 概要

このPythonスクリプトは、指定されたファイル内で特定の単語を検索し、結果をCSVファイルに出力するツールです。また、処理の概要をAPIに送信する機能も備えています。

## 主要な機能

1. **ファイル内の単語検索**: 指定されたファイル内で、予め定義された単語リストの単語を検索します。
2. **CSV出力**: 検索結果をCSVファイルに出力します。
3. **ログ記録**: 処理の詳細をログファイルに記録します。
4. **API通知**: 処理の概要を指定されたAPIエンドポイントに送信します。

## 使用方法

### 前提条件

- Python 3.6以上
- 必要なライブラリ: `requests`

### スクリプトの実行

1. スクリプトの末尾にある `__main__` ブロックで、以下のパラメータを設定します：

   ```python
   input_file = 'file_paths.csv'  # 処理対象のファイルパスが記載されたCSVファイル
   word1_list = ['word1', 'alias1']  # 検索する単語リスト1
   word2_list = ['word2', 'alias2']  # 検索する単語リスト2
   output_file = 'results.csv'  # 結果を出力するCSVファイル
   api_url = 'https://example.com/api/results'  # 結果を送信するAPIのURL
   ```

2. コマンドラインから次のコマンドでスクリプトを実行します：

   ```
   python script_name.py
   ```

### 主要な関数

#### `check_words_in_file(file_path: str, word_set: set) -> Tuple[bool, List[str], Optional[str]]`

指定されたファイル内で単語セットの単語を検索します。

- **引数**:
  - `file_path`: 検索対象のファイルパス
  - `word_set`: 検索する単語のセット
- **戻り値**:
  - `bool`: 単語が見つかったかどうか
  - `List[str]`: 見つかった単語のリスト
  - `Optional[str]`: エラーメッセージ（エラーがない場合はNone）

#### `process_file_paths(input_file: str, word1_list: List[str], word2_list: List[str], output_file: Optional[str] = None, api_url: Optional[str] = None) -> None`

CSVファイルからファイルパスを読み取り、各ファイルで単語検索を実行し、結果をCSVファイルに出力します。

- **引数**:
  - `input_file`: 入力CSVファイルのパス
  - `word1_list`: 検索する単語リスト1
  - `word2_list`: 検索する単語リスト2
  - `output_file`: 結果を出力するCSVファイルのパス（オプション）
  - `api_url`: 結果を送信するAPIのURL（オプション）

## 注意点

1. **セキュリティ**:
   - ファイルパスの検証を行い、ディレクトリトラバーサル攻撃を防止しています。
   - API通信にはHTTPS使用を推奨します。

2. **パフォーマンス**:
   - 大量のファイルを処理する場合、処理時間が長くなる可能性があります。

3. **エラー処理**:
   - ファイル処理中のエラーはログに記録され、スクリプトの実行は継続されます。

4. **ログ**:
   - ログファイル `file_processing.log` に詳細な処理情報が記録されます。

5. **API通信**:
   - API通信に失敗した場合でも、ローカルでの処理は完了します。

## カスタマイズ

- 検索する単語リストは、必要に応じて `word1_list` と `word2_list` を変更することで調整
- ログレベルは `logging.basicConfig()` の `level` パラメータで調整

```
import logging
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from src.file_readers.excel_reader import read_excel
from src.file_readers.word_reader import read_word
from src.file_readers.powerpoint_reader import read_powerpoint
from src.file_readers.text_reader import read_text
from src.file_readers.zip_reader import read_zip
from src.file_readers.csv_reader import read_csv
from src.utils.error_handler import send_error_notification
import requests
import datetime
import socket
import os

class FileProcessor:
    def __init__(self, keyword_A_list, keyword_B_list, webhook_url, error_threshold, api_url=None):
        """
        初期化メソッド

        :param keyword_A_list: 検索対象のキーワードAのリスト
        :param keyword_B_list: 検索対象のキーワードBのリスト
        :param webhook_url: エラー通知用のWebhook URL
        :param error_threshold: エラー通知を送信する閾値
        :param api_url: 処理完了後に結果を送信するAPIのURL（オプション）
        """
        self.keyword_A_list = keyword_A_list
        self.keyword_B_list = keyword_B_list
        self.webhook_url = webhook_url
        self.error_threshold = error_threshold
        self.api_url = api_url
        self.error_buffer = []
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # カウンタの初期化
        self.total_files = 0
        self.error_count = 0

    def process_file(self, file_path):
        """
        個々のファイルを処理します。

        :param file_path: 処理対象のファイルパス
        """
        try:
            content = self.read_file(file_path)
            if content is not None:
                keyword_match, matched_keywords = self.search_keywords(content)
                
                # ファイル処理成功のカウント
                self.total_files += 1

                # テキストログに詳細を記録
                self.logger.info(f"Processed file: {file_path}")
                if keyword_match:
                    self.logger.info(f"Keywords found in file: {file_path}. Matched keywords: {', '.join(matched_keywords)}")
                else:
                    self.logger.info(f"No keywords found in file: {file_path}")
                
                # CSVに結果を記録 (すべてのファイル)
                self.logger.info('', extra={
                    'csv_result': True,
                    'file_path': file_path,
                    'status': 'Matched' if keyword_match else 'Not Matched',
                    'matched_keywords': ', '.join(matched_keywords) if keyword_match else 'None'
                })
            else:
                self.logger.warning(f"Unable to read file: {file_path}")
                self.error_count += 1
                # 読み取り不可能なファイルもCSVに記録
                self.logger.info('', extra={
                    'csv_result': True,
                    'file_path': file_path,
                    'status': 'Unreadable',
                    'error_message': 'Unable to read file'
                })
        
        except Exception as e:
            error_message = f"Error processing file {file_path}: {str(e)}"
            self.logger.error(error_message)
            self.handle_error(error_message)
            self.error_count += 1
            # エラーが発生したファイルもCSVに記録
            self.logger.info('', extra={
                'csv_result': True,
                'file_path': file_path,
                'status': 'Error',
                'error_message': str(e)
            })

    def read_file(self, file_path):
        """
        ファイルタイプに応じて適切なリーダーを使用してファイルを読み取ります。

        :param file_path: 読み取るファイルのパス
        :return: ファイルの内容またはNone
        """
        if file_path.endswith(('.xlsx', '.xls', '.xlsb', '.xlsm')):
            return read_excel(file_path)
        elif file_path.endswith(('.docx', '.doc')):
            return read_word(file_path)
        elif file_path.endswith(('.pptx', '.ppt')):
            return read_powerpoint(file_path)
        elif file_path.endswith('.txt'):
            return read_text(file_path)
        elif file_path.endswith('.zip'):
            return read_zip(file_path)
        elif file_path.endswith('.csv'):
            return read_csv(file_path)
        else:
            self.logger.warning(f"Unsupported file type: {file_path}")
            return None

    def search_keywords(self, content):
        """
        コンテンツ内でキーワードを検索します。

        :param content: 検索対象のコンテンツ
        :return: キーワードが見つかったかどうかと、マッチしたキーワードのリスト
        """
        matched_keywords = []
        for keyword in self.keyword_A_list + self.keyword_B_list:
            if keyword in content:
                matched_keywords.append(keyword)
        return bool(matched_keywords), matched_keywords

    def handle_error(self, error_message):
        """
        エラーハンドリングを行います。

        :param error_message: エラーメッセージ
        """
        self.logger.error(error_message)
        self.error_buffer.append(error_message)
        if len(self.error_buffer) >= self.error_threshold:
            send_error_notification(self.webhook_url, self.error_buffer)
            self.error_buffer.clear()

    def process_excel(self, excel_file_path):
        """
        Excelファイルからファイルパスを読み取り、各ファイルを処理します。
        処理完了後にAPIへ結果を送信します。

        :param excel_file_path: 処理対象のExcelファイルのパス
        """
        start_time = datetime.datetime.now()
        self.logger.info(f"Excelファイルの処理を開始します: {excel_file_path}")

        try:
            file_paths = read_excel(excel_file_path)
            
            if not file_paths:
                self.logger.warning(f"Excelファイルにファイルパスが見つかりません: {excel_file_path}")
                return

            with ThreadPoolExecutor() as executor:
                list(tqdm(executor.map(self.process_file, file_paths), total=len(file_paths)))

            self.logger.info(f"Excelファイルの処理が完了しました: {excel_file_path}")

        except Exception as e:
            error_message = f"Error processing Excel file {excel_file_path}: {str(e)}"
            self.handle_error(error_message)
            self.error_count += 1

        end_time = datetime.datetime.now()

        # API連携
        if self.api_url:
            data = {
                "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S'),
                "end_time": end_time.strftime('%Y-%m-%d %H:%M:%S'),
                "total_files": self.total_files,
                "error_count": self.error_count,
                "input_file": os.path.basename(excel_file_path),
                "host_name": socket.gethostname()
            }
            try:
                response = requests.post(self.api_url, json=data)
                if response.status_code == 200:
                    self.logger.info(f"Successfully posted results to API: {self.api_url}")
                else:
                    self.logger.error(f"Failed to post results to API. Status code: {response.status_code}")
            except Exception as e:
                self.logger.error(f"Error occurred while posting results to API: {str(e)}")

    def process_zip(self, zip_file_path):
        """
        ZIPファイルを処理します。

        :param zip_file_path: 処理対象のZIPファイルのパス
        """
        try:
            file_contents = read_zip(zip_file_path)
            for file_name, content in file_contents.items():
                keyword_match, matched_keywords = self.search_keywords(content)
                
                extra = {
                    'file_path': f"{zip_file_path}/{file_name}",
                    'keyword_match': 'Yes' if keyword_match else 'No',
                    'matched_keywords': ', '.join(matched_keywords) if matched_keywords else 'None'
                }
                self.logger.info(f"Processed file in ZIP: {file_name}", extra=extra)
                
                if keyword_match:
                    self.logger.info(f"Keywords found in ZIP file: {file_name}. Matched keywords: {extra['matched_keywords']}", extra=extra)
                else:
                    self.logger.info(f"No keywords found in ZIP file: {file_name}", extra=extra)
        
        except Exception as e:
            extra = {
                'file_path': zip_file_path,
                'keyword_match': 'Error'
            }
            self.logger.error(f"Error processing ZIP file {zip_file_path}: {str(e)}", extra=extra)
            self.handle_error(f"Error processing ZIP file {zip_file_path}: {str(e)}")
            self.error_count += 1
```
