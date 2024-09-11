import os
import csv
import logging
import requests
import socket
from datetime import datetime
from typing import List, Tuple, Optional, Dict
from pathlib import Path

# Logging configuration
logging.basicConfig(filename='file_processing.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def check_words_in_file(file_path: str, word_set: set) -> Tuple[bool, List[str], Optional[str]]:
    """
    Checks if any word in word_set is present in the file.

    Parameters:
    - file_path (str): The file to check.
    - word_set (set): Set of words to search for.

    Returns:
    - status (bool): True if any word is found, False otherwise.
    - matched_words (list): List of matched words.
    - error_message (str): Error message if any, None otherwise.
    """
    matched_words = []
    try:
        file_path = Path(file_path).resolve()
        if not file_path.is_file() or not str(file_path).startswith(str(Path.cwd())):
            raise ValueError("Invalid or insecure file path")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            matched_words = [word for word in word_set if word in content]
            
        return bool(matched_words), matched_words, None
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {str(e)}")
        return False, [], str(e)

def process_file_paths(input_file: str, word1_list: List[str], word2_list: List[str], 
                       output_file: Optional[str] = None, api_url: Optional[str] = None) -> None:
    """
    Reads file paths from a CSV file, checks for the presence of words in the files,
    and outputs the results to a CSV file, logging all actions. At the end, sends the summary to a specified API.

    Parameters:
    - input_file (str): Path to the input CSV file containing file paths.
    - word1_list (List[str]): List of words to search for.
    - word2_list (List[str]): List of words to search for.
    - output_file (Optional[str]): Path to the output CSV file to save results.
    - api_url (Optional[str]): API URL to send the summary results to.
    """
    results = []
    start_time = datetime.now()
    error_count = 0
    total_files = 0

    word_set = set(word1_list + word2_list)

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            file_paths = [row[0] for row in reader]
            total_files = len(file_paths)
    except Exception as e:
        logging.error(f"Error reading input file {input_file}: {str(e)}")
        return

    for file_path in file_paths:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status, matched_words, error_message = check_words_in_file(file_path, word_set)
        status_text = "Success" if status else "Failure"
        matched_str = ','.join(matched_words) if matched_words else 'None'
        results.append([timestamp, file_path, status_text, matched_str, error_message or ''])
        
        log_level = logging.INFO if status else logging.ERROR
        logging.log(log_level, f"File {file_path} processed: {status_text}, Matched: {matched_str}")
        
        if error_message:
            error_count += 1

    end_time = datetime.now()

    if output_file:
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'File Path', 'Status', 'Matched Words', 'Error Message'])
                writer.writerows(results)
            logging.info(f"Results saved to {output_file}")
        except Exception as e:
            logging.error(f"Error writing to output file {output_file}: {str(e)}")

    if api_url:
        data = {
            "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": end_time.strftime('%Y-%m-%d %H:%M:%S'),
            "total_files": total_files,
            "error_count": error_count,
            "input_file": os.path.basename(input_file),
            "host_name": socket.gethostname()
        }
        try:
            response = requests.post(api_url, json=data)
            if response.status_code == 200:
                logging.info(f"Successfully posted results to API: {api_url}")
            else:
                logging.error(f"Failed to post results to API. Status code: {response.status_code}")
        except Exception as e:
            logging.error(f"Error posting results to API: {str(e)}")

if __name__ == "__main__":
    # Example usage
    input_file = 'file_paths.csv'
    word1_list = ['word1', 'alias1']
    word2_list = ['word2', 'alias2']
    output_file = 'results.csv'
    api_url = 'https://example.com/api/results'

    process_file_paths(input_file, word1_list, word2_list, output_file, api_url)
