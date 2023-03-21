from django.shortcuts import render
import requests
import pandas as pd
import math
import os
from dotenv import load_dotenv
endpoint = "https://dir.aviapages.com/api/aircraft/"
load_dotenv('api_token.env')
api_token = os.environ.get('API_TOKEN')
headers = {'Authorization' : api_token}
print(api_token)
def apisearch(request):
    Keys = {'search_tail_number':'1',
            'images':True,
            'per_page': '40'}

    if request.method == 'POST':
        search_word = request.POST.get("avia_search_value")
        if search_word.isdigit():
            Keys['search_serial_number'] = search_word
        else:
            Keys['search_tail_number'] = search_word

    # Set the number of results you want to retrieve
    num_results = 300

    # Calculate the number of pages needed
    num_pages = math.ceil(num_results / 20)

    # Make requests for each page and append the results
    results = []
    for page in range(1, num_pages + 1):
        Keys['per_page'] = 20
        Keys['page'] = page
        response = requests.get(endpoint,params=Keys,headers=headers).json()
        aircrafts = response.get("results", [])
        results.extend(aircrafts)
        if len(results) >= num_results:
            break

    # Create the data dictionary
    data = {
        'images': [],
        'tail_number': [],
        'serial_number': [],
        'aircraft_type_name': [],
        'year_of_production': [],
    }

    for aircraft in results:
        # Extract the URLs from the images dictionaries
        if isinstance(aircraft['images'], list) and aircraft['images']:
            images = [img['url'] for img in aircraft['images'][:3] if 'url' in img]
        else:
            images = ['https://via.placeholder.com/70x70.png?text=No+Image']
        # Append the data to the corresponding lists
        data['images'].append(images)
        data['tail_number'].append(aircraft['tail_number'])
        data['serial_number'].append(aircraft['serial_number'])
        data['aircraft_type_name'].append(aircraft['aircraft_type_name'])
        data['year_of_production'].append(aircraft['year_of_production'])

    # Convert the URLs to HTML tags
    df = pd.DataFrame(data)
    if isinstance(data['images'], list):
        df['images'] = df['images'].apply(
            lambda urls: ''.join([f'<img src="{url}" width="250" height="250">' for url in urls])
        )
    end={'html_table':df.to_html(index=False, escape=False, classes='table table-hover')}
    return render(request, 'main/search.html',end)

def index(request):
    return render(request, 'main/index.html',{'name':1})
