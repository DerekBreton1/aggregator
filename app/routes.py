from flask import render_template, request
from app import app

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    # Process form data and return results
    return render_template('index.html', results=2)#some_results)

