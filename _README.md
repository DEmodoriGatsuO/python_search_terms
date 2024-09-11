# File Processing Script Documentation

## 概要

このPythonスクリプトは、指定されたファイル内で特定の単語を検索し、結果をCSVファイルに出力するツールです。また、処理の概要をAPIに送信する機能も備えています。

## 主要な機能

1. **ファイル内の単語検索**: 指定されたファイル内で、予め定義された単語リストの単語を検索します。
2. **CSV出力**: 検索結果をCSVファイルに出力します。
3. **ログ記録**: 処理の詳細をログファイルに記録します。
4. **API通知**: 処理の概要を指定されたAPIエンドポイントに送信します。

## 使用方法

### 前提条件

- Python 3.6以上
- 必要なライブラリ: `requests`

### スクリプトの実行

1. スクリプトの末尾にある `__main__` ブロックで、以下のパラメータを設定します：

   ```python
   input_file = 'file_paths.csv'  # 処理対象のファイルパスが記載されたCSVファイル
   word1_list = ['word1', 'alias1']  # 検索する単語リスト1
   word2_list = ['word2', 'alias2']  # 検索する単語リスト2
   output_file = 'results.csv'  # 結果を出力するCSVファイル
   api_url = 'https://example.com/api/results'  # 結果を送信するAPIのURL
   ```

2. コマンドラインから次のコマンドでスクリプトを実行します：

   ```
   python script_name.py
   ```

### 主要な関数

#### `check_words_in_file(file_path: str, word_set: set) -> Tuple[bool, List[str], Optional[str]]`

指定されたファイル内で単語セットの単語を検索します。

- **引数**:
  - `file_path`: 検索対象のファイルパス
  - `word_set`: 検索する単語のセット
- **戻り値**:
  - `bool`: 単語が見つかったかどうか
  - `List[str]`: 見つかった単語のリスト
  - `Optional[str]`: エラーメッセージ（エラーがない場合はNone）

#### `process_file_paths(input_file: str, word1_list: List[str], word2_list: List[str], output_file: Optional[str] = None, api_url: Optional[str] = None) -> None`

CSVファイルからファイルパスを読み取り、各ファイルで単語検索を実行し、結果をCSVファイルに出力します。

- **引数**:
  - `input_file`: 入力CSVファイルのパス
  - `word1_list`: 検索する単語リスト1
  - `word2_list`: 検索する単語リスト2
  - `output_file`: 結果を出力するCSVファイルのパス（オプション）
  - `api_url`: 結果を送信するAPIのURL（オプション）

## 注意点

1. **セキュリティ**:
   - ファイルパスの検証を行い、ディレクトリトラバーサル攻撃を防止しています。
   - API通信にはHTTPS使用を推奨します。

2. **パフォーマンス**:
   - 大量のファイルを処理する場合、処理時間が長くなる可能性があります。

3. **エラー処理**:
   - ファイル処理中のエラーはログに記録され、スクリプトの実行は継続されます。

4. **ログ**:
   - ログファイル `file_processing.log` に詳細な処理情報が記録されます。

5. **API通信**:
   - API通信に失敗した場合でも、ローカルでの処理は完了します。

## カスタマイズ

- 検索する単語リストは、必要に応じて `word1_list` と `word2_list` を変更することで調整
- ログレベルは `logging.basicConfig()` の `level` パラメータで調整
