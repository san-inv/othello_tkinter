.PHONY: run test lint clean help

# デフォルトターゲット
help:
	@echo "使用可能なコマンド:"
	@echo "  make run    - ゲームを起動"
	@echo "  make test   - テストを実行"
	@echo "  make lint   - コードスタイルをチェック"
	@echo "  make clean  - キャッシュファイルを削除"
	@echo "  make help   - このヘルプを表示"

# ゲームを起動
run:
	python othello.py

# テストを実行
test:
	pytest tests/ -v

# コードスタイルをチェック
lint:
	flake8 othello.py --max-line-length=100
	@echo "コードスタイルチェック完了"

# キャッシュファイルを削除
clean:
	rm -rf __pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache
	rm -rf *.pyc
	rm -rf .mypy_cache
	@echo "キャッシュを削除しました"
