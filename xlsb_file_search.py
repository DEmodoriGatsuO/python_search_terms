import os
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pyxlsb import open_workbook

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

def read_all_sheets_xlsb_file_paths(xlsb_file):
    """
    Reads file paths from all sheets of an XLSB file.
    
    Parameters:
    - xlsb_file (str): Path to the XLSB file.
    
    Returns:
    - file_paths (list): List of file paths extracted from all sheets in the XLSB file.
    """
    file_paths = []
    try:
        with open_workbook(xlsb_file) as wb:
            for sheet_name in wb.sheets:
                print(f"Processing sheet: {sheet_name}")
                with wb.get_sheet(sheet_name) as sheet:
                    for row in sheet.rows():
                        file_path = row[0].v  # Assuming the file path is in the first column
                        if file_path:  # Ensure it's not None or empty
                            file_paths.append(file_path)
    except Exception as e:
        print(f"Error reading XLSB file {xlsb_file}: {e}")
    
    return file_paths

def check_file_existence(input_xlsb, output_csv=None, max_workers=10):
    """
    Checks if the files listed in the XLSB file (from all sheets) exist on the system and outputs the results.
    This version uses multithreading to improve performance with large file counts.

    Parameters:
    - input_xlsb (str): Path to the input XLSB file containing file paths.
    - output_csv (str, optional): Path to save the output CSV file with results. If None, results will be printed.
    - max_workers (int, optional): Number of threads to use for parallel processing.
    """
    results = []

    # Read file paths from all sheets of the XLSB file
    file_paths = read_all_sheets_xlsb_file_paths(input_xlsb)
    
    if not file_paths:
        print(f"No file paths found in {input_xlsb}. Exiting...")
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
input_xlsb = 'file_paths.xlsb'  # Path to the input XLSB file
output_csv = 'file_check_results.csv'  # Optional: Path to save the output CSV file with results
max_workers = 20  # Number of threads for parallel processing

check_file_existence(input_xlsb, output_csv, max_workers)