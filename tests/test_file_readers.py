import pytest
import os
from src.file_readers.excel_reader import read_excel
from src.file_readers.word_reader import read_word
from src.file_readers.powerpoint_reader import read_powerpoint
from src.file_readers.text_reader import read_text
from src.file_readers.zip_reader import read_zip
from src.file_readers.csv_reader import read_csv

# テストファイルのディレクトリ
TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), 'test_files')

def test_read_excel():
    excel_file = os.path.join(TEST_FILES_DIR, 'test.xlsx')
    content = read_excel(excel_file)
    assert "テストデータ" in content
    assert "Sheet1" in content

def test_read_word():
    word_file = os.path.join(TEST_FILES_DIR, 'test.docx')
    content = read_word(word_file)
    assert "これはテストドキュメントです" in content

def test_read_powerpoint():
    ppt_file = os.path.join(TEST_FILES_DIR, 'test.pptx')
    content = read_powerpoint(ppt_file)
    assert "テストスライド" in content

def test_read_text():
    txt_file = os.path.join(TEST_FILES_DIR, 'test.txt')
    content = read_text(txt_file)
    assert "This is a test text file" in content

def test_read_non_existent_file():
    non_existent_file = os.path.join(TEST_FILES_DIR, 'non_existent.txt')
    content = read_text(non_existent_file)
    assert content == ""

def test_read_zip():
    zip_file = os.path.join(TEST_FILES_DIR, 'test.zip')
    contents = read_zip(zip_file)
    assert len(contents) > 0
    assert any("テストデータ" in content for content in contents.values())

def test_read_csv():
    csv_file = os.path.join(TEST_FILES_DIR, 'test.csv')
    content = read_csv(csv_file)
    assert len(content) > 0
    assert "テストデータ" in content[0]

# エラーケースのテスト
def test_read_zip_with_invalid_file():
    invalid_file = os.path.join(TEST_FILES_DIR, 'invalid.zip')
    with pytest.raises(Exception):
        read_zip(invalid_file)

def test_read_csv_with_invalid_file():
    invalid_file = os.path.join(TEST_FILES_DIR, 'invalid.csv')
    content = read_csv(invalid_file)
    assert content == []