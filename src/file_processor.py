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

class FileProcessor:
    def __init__(self, keyword_A_list, keyword_B_list, webhook_url, error_threshold):
        self.keyword_A_list = keyword_A_list
        self.keyword_B_list = keyword_B_list
        self.webhook_url = webhook_url
        self.error_threshold = error_threshold
        self.error_buffer = []
        self.logger = logging.getLogger(__name__)

    def process_file(self, file_path):
        try:
            content = self.read_file(file_path)
            if content is not None:
                keyword_match, matched_keywords = self.search_keywords(content)
                
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
            # エラーが発生したファイルもCSVに記録
            self.logger.info('', extra={
                'csv_result': True,
                'file_path': file_path,
                'status': 'Error',
                'error_message': str(e)
            })

    def read_file(self, file_path):
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
        matched_keywords = []
        for keyword in self.keyword_A_list + self.keyword_B_list:
            if keyword in content:
                matched_keywords.append(keyword)
        return bool(matched_keywords), matched_keywords

    def handle_error(self, error_message):
        self.logger.error(error_message)
        self.error_buffer.append(error_message)
        if len(self.error_buffer) >= self.error_threshold:
            send_error_notification(self.webhook_url, self.error_buffer)
            self.error_buffer.clear()

    def process_csv(self, csv_file_path):
        try:
            file_paths = read_csv(csv_file_path)
            
            if not file_paths:
                self.logger.warning(f"No file paths found in CSV: {csv_file_path}")
                return

            with ThreadPoolExecutor() as executor:
                list(tqdm(executor.map(self.process_file, file_paths), total=len(file_paths)))

            self.logger.info(f"Completed processing of CSV: {csv_file_path}")
        except Exception as e:
            self.handle_error(f"Error processing CSV file {csv_file_path}: {str(e)}")

    def process_zip(self, zip_file_path):
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