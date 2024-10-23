from flask import Flask
from app import app
from app.routes import register_routes

app = Flask(__name__)

# Register routes
register_routes(app)

if __name__ == "__main__":
    from gunicorn.app.wsgiapp import run
    app.run()