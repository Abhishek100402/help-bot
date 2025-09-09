from flask import Flask
from pathlib import Path
from dotenv import load_dotenv
import os


# load .env from project root if present
root = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=root / '.env')




def create_app():
    app = Flask(
        __name__,
        template_folder=str(root / 'templates'),
        static_folder=str(root / 'static'),
        static_url_path="/static"  # <-- add this line
    )
    app.config['GEMINI_MODEL'] = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
    app.config['GEMINI_API_KEY'] = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'change-this-in-prod')


    # basic sanity check
    if not app.config['GEMINI_API_KEY']:
        raise RuntimeError('GEMINI_API_KEY is not set. Add it to your .env or environment variables.')


    # register routes
    from .routes import bp as chat_bp
    app.register_blueprint(chat_bp)


    return app