import os
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

def check_file(file_path):
    """
    Checks if a single file exists and returns the result.
    Parameters:
    - file_path (str): The file path to check.
    
    Returns:
    - result (list): A list containing the timestamp, file path, and existence status.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if os.path.exists(file_path):
        return [timestamp, file_path, 'Exists']
    else:
        return [timestamp, file_path, 'Not Found']

def check_file_existence(input_csv, output_csv=None, max_workers=10):
    """
    Checks if the files listed in the input CSV exist on the system and outputs the results.
    This version uses multithreading to improve performance with large file counts.

    Parameters:
    - input_csv (str): Path to the input CSV file containing file paths.
    - output_csv (str, optional): Path to save the output CSV file with results. If None, results will be printed.
    - max_workers (int, optional): Number of threads to use for parallel processing.
    """
    results = []

    # Read file paths from the CSV file
    try:
        with open(input_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            file_paths = [row[0] for row in reader]
    except Exception as e:
        print(f"Error reading input file {input_csv}: {e}")
        return

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_file, file_path): file_path for file_path in file_paths}
        
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error processing file {futures[future]}: {e}")

    # Output results to CSV or print to console
    if output_csv:
        try:
            with open(output_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'File Path', 'Status'])
                writer.writerows(results)
            print(f"Results saved to {output_csv}")
        except Exception as e:
            print(f"Error writing to output file {output_csv}: {e}")
    else:
        # Print results to the console
        print("File Path Check Results:")
        for result in results:
            print(result)

# Example usage
input_csv = 'file_paths.csv'  # Path to the input CSV file
output_csv = 'file_check_results.csv'  # Optional: Path to save the output CSV file with results
max_workers = 20  # Number of threads for parallel processing

check_file_existence(input_csv, output_csv, max_workers)