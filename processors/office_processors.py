from .base_processor import BaseFileProcessor 
class OfficeFileProcessor(BaseFileProcessor): 
    def __init__(self, read_function): 
        self.read_function = read_function 
    def extract_text(self, file_path): 
        return self.read_function(file_path) 
