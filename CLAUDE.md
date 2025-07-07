# Claude Code Configuration

This file helps Claude Code understand your project structure and preferences.

## Project Overview
FastAPIを用いた自作パソコンについてのwebサービス。
バックエンドは作ったのでフロントエンドを整えて欲しい。
価格ドットコムのようなレイアウトが好まれる。

## Development Commands
- `python -m uvicorn main:app --reload` - Start development server
- `pip install -r requirements.txt` - Install dependencies
- `pytest` - Run tests
- `black .` - Format code
- `flake8` - Lint code

## Project Structure
- `main.py` - FastAPI application entry point
- `models/` - Database models
- `routers/` - API route handlers
- `static/` - Static files (CSS, JS, images)
- `templates/` - HTML templates
- `requirements.txt` - Python dependencies
- `frontend/` - html,css,JavaScriptファイルが入っている
- `frontend/ex` - サンプルデータが入っている。編集しない
- `frontend/img/logo.png` - このwebサービスのロゴマーク

## Notes
- Uses SQLAlchemy for database ORM
- Jinja2 templates for HTML rendering
- Static files served directly by FastAPI
- 変更を加えられるファイルはhtmlとcssファイルのみ
- htmlファイル内のJavaScriptは変更しない
- 会話は全て日本語で行う
- 指示が曖昧なときは聞く
- githubにコミット、プッシュする際はhttps://github.com/Tiizu727/myj-fastapi-web-app-main.gitにする