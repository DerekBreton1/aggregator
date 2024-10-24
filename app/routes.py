from flask import Blueprint, render_template, request, jsonify
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import re

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def home():
    return render_template("index.html")

@app_routes.route('/query', methods=['GET','POST'])
def query():
    search_base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    # Get JSON data from the frontend
    data = request.get_json()
    database = data.get('param1')
    search_term = data.get('param2')
        
    # Run eSearch  
    # Define base url and input terms (will come from form)
    search_base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    db = 'gds'
    term = 'asthma'

    # Construct query
    search_query_string = search_base_url + "?" + "db=" + db + "&" + "term=" + term

    # Make a GET request to retrieve the XML data
    url = search_query_string
    response = requests.get(url)

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

    else:
        print("Error: {}".format(response.status_code))


    # Run eSummary
    summary_base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

    # Create DataFrame to store summary results
    summary_df = pd.DataFrame()

    # Gather summary for every ID
    for id in id_list:
        # Define summary query string
        summary_query_string = summary_base_url + "?" + "db=" + db + "&" + "id=" + id

        # Make a GET request to retrieve the XML data
        url = summary_query_string
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the XML response
            summary_root = ET.fromstring(response.content)

        else:
            print("Error: {}".format(response.status_code))

        regex = r"'Name':\s*'([^']+)'"
        match_dict = {}

        # Iterate through summary results
        for i in summary_root.iter():
            # Extract attribute names
            attrib_match = re.search(regex, str(i.attrib))

            if attrib_match:
                match_dict[attrib_match.group(1)] = i.text

        # Create DataFrame from this set of results
        temp_df = pd.DataFrame(match_dict, index=[0])
        temp_df['id'] = id

        #Concatenate DataFrames
        summary_df = pd.concat([summary_df, temp_df])

    # Fix index
    summary_df.reset_index(inplace=True)
    # Remove columns contianing only missing/ na values
    summary_df.dropna(axis=1, how='all', inplace=True)
    # Drop predetermined columns
    summary_df.drop(['index', 'summary', 'Samples', 'Sample', 'int', 'PubMedIds'], axis=1, inplace=True)
    # Drop duplicated rows (unique ids map to non-unique entires)
    summary_df.drop_duplicates(subset='Accession', inplace=True)
    
    #return jsonify({'message': 'Query recieved successfully'}), 200
    return(summary_df.to_json())

#else:
#    print("Error: {}".format(response.status_code))