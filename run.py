from flask import Flask
from app import app
from app.routes import register_routes
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

# Register routes
register_routes(app)

if __name__ == "__main__":
    from gunicorn.app.wsgiapp import run
    app.run()