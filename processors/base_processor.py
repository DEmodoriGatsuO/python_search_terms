from abc import ABC, abstractmethod 
class BaseFileProcessor(ABC): 
    @abstractmethod 
    def extract_text(self, file_path): 
        pass 
