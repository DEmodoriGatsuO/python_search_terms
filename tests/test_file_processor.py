import pytest
from src.file_processor import FileProcessor

def test_search_keywords():
    processor = FileProcessor(["test"], ["Company"], "https://example.com/webhook", 10)
    text = "This is a test document for Company"
    assert processor.search_keywords(text, "test.txt") == True

# その他のテストケースを追加