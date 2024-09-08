# Python File Search Script

## Overview

The Python File Search Script is a powerful tool designed to search through various file formats (Excel, Word, PowerPoint, Text, ZIP, CSV) and report the occurrences of specified keywords. It efficiently processes large volumes of files, allowing users to quickly locate specific information across multiple documents.

## Key Features

- Support for multiple file formats (.xlsx, .xls, .xlsb, .docx, .doc, .pptx, .ppt, .txt, .zip, .csv)
- AND search functionality (combination of Keyword A and Keyword B)
- Recursive search within ZIP files
- Individual row search in CSV files
- Multi-threaded processing for improved performance
- Detailed logging
- Error notification system (using Webhooks)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/python-file-search.git
   cd python-file-search
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Edit the `config/settings.yaml` file to configure:
   - Keyword lists
   - Webhook URL for notifications
   - Logging level

## Usage

1. Prepare a CSV file containing the file paths to be searched. The CSV should be formatted as follows:
   ```
   file_path
   /path/to/file1.xlsx
   /path/to/file2.docx
   /path/to/archive.zip
   ```

2. Run the script:
   ```
   python main.py
   ```

3. Once the process is complete, results will be recorded in the log file. Error notifications will be sent to the configured Webhook (if any errors occur).

## Important Notes

- Be mindful of memory usage and disk space when processing large numbers of files or large ZIP files.
- Processing very large CSV files may impact performance as each row is processed individually.
- Temporary directories are used for ZIP file processing. Ensure sufficient disk space is available.
- For security reasons, only process files from trusted sources.

## Troubleshooting

- If the script terminates unexpectedly, check the log file for error messages.
- If certain files are not being processed, verify the file format and permissions.
- For performance issues, consider reducing the number of files processed or running the script on more powerful hardware.

## Contributing

Please use the GitHub Issue Tracker to report bugs or request features. Pull requests are welcome.

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Performance and Scalability

- The script uses multi-threading to improve processing speed, but performance may vary based on the number and size of files.
- For very large datasets, consider breaking the process into smaller batches.
- Monitor system resources (CPU, memory, disk I/O) when processing large volumes of data.

## Security Considerations

- The script processes files on the local system. Ensure you have appropriate permissions for all files and directories.
- Be cautious when processing files from unknown sources, as they may contain malicious content.
- Sensitive information in processed files will be logged. Ensure log files are stored securely.

## Updates and Maintenance

This script is actively maintained. Please check the repository regularly for updates and improvements.

For any questions or support, please open an issue on the GitHub repository.