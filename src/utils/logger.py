import logging
from logging.handlers import RotatingFileHandler
import csv
from datetime import datetime

class CSVResultHandler(logging.Handler):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.csv_file = open(self.filename, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp', 'File Path', 'Status', 'Matched Keywords', 'Error Message'])

    def emit(self, record):
        if hasattr(record, 'csv_result'):
            timestamp = datetime.fromtimestamp(record.created).isoformat()
            self.csv_writer.writerow([
                timestamp,
                record.file_path,
                record.status,
                record.matched_keywords if hasattr(record, 'matched_keywords') else '',
                record.error_message if hasattr(record, 'error_message') else ''
            ])
            self.csv_file.flush()

    def close(self):
        self.csv_file.close()
        super().close()

def setup_logger(log_level, log_format, log_file_base):
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # テキストログハンドラの設定
    txt_handler = RotatingFileHandler(
        f"{log_file_base}.txt", maxBytes=10*1024*1024, backupCount=5
    )
    txt_formatter = logging.Formatter(log_format)
    txt_handler.setFormatter(txt_formatter)
    logger.addHandler(txt_handler)

    # CSV結果ハンドラの設定
    csv_handler = CSVResultHandler(f"{log_file_base}_results.csv")
    logger.addHandler(csv_handler)

    # コンソール出力用ハンドラ
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(txt_formatter)
    logger.addHandler(console_handler)

    return logger