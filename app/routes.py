from flask import render_template, request, jsonify
from app import app
import requests
import xml.etree.ElementTree as ET
import pandas as pd

#@app.route('/')
#def home():
#    return render_template('index.html')

def register_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')


    @app.route('/query', methods=['POST'])
    def query():
        search_base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

        # Get JSON data from the frontend
        data = request.get_json()
        database = data.get('param1')
        search_term = data.get('param2')
        
        # Construct query URL
        search_url = search_base + '?' + 'db=' + database + '&' + 'term=' + search_term

        # Make a GET request to retrieve the XML data
        response = requests.get(search_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the XML response
            root = ET.fromstring(response.content)

            # Process the XML data (e.g., extract specific elements)
            id_list = []

            # Iterate through tree
            for child in root.iter():
                # Save UIDs 
                if child.tag == "Id":
                    id_list.append(child.text)
            
            query_results = pd.DataFrame({'id':id_list})

        else:
            print("Error: {}".format(response.status_code))
        
        # Process form data and return results

        return render_template('index.html', results=jsonify(query_results))

