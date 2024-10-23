from flask import Flask
from app import app

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello from Flask on Vercel!"

if __name__ == "__main__":
    from gunicorn.app.wsgiapp import run
    app.run()