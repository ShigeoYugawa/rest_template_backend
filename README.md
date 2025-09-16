
# Django REST テンプレート（バックエンド）

このプロジェクトは Django REST API のテンプレートです。特徴は以下の通りです：

- Custom User モデル（accounts アプリ）
- 国際化対応（日本語対応、`LANGUAGE_CODE=ja`、`TIME_ZONE=Asia/Tokyo`）
- 型チェック対応（`mypy` + `django-stubs`）
- 将来的に Docker や React フロントエンドと連携可能

---

## 必要環境
- Python 3.12 以上
- Django 5.x
- Virtualenv 推奨

---

## セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/yourname/django-rest-template.git
cd django-rest-template/rest_template_backend

# 仮想環境を作成・有効化
python -m venv .venv
source .venv/bin/activate

# 依存パッケージをインストール
pip install -r requirements.txt
````

---

## サーバー起動

```bash
python manage.py migrate
python manage.py runserver
```

サーバーは以下で起動します：
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 開発用コマンド

### 型チェック

```bash
mypy .
```

### テスト

(準備中：pytest を統合予定)

```bash
pytest
```

### 国際化（日本語）

翻訳ファイルを作成・コンパイル：

```bash
python manage.py makemessages -l ja
python manage.py compilemessages
```

---

## 注意点

* `.gitignore` は Django、Python、仮想環境、mypy、IDE ファイル用に設定済み
* SQLite (`db.sqlite3`) は Git に含めない設定です
* Docker や CI/CD パイプラインは必要に応じて後から追加可能です

