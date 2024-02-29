# backend\patent_analysis.py

import json
import openai
import logging
import os
from datetime import datetime
import spacy
from fuzzywuzzy import fuzz
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
from .models import IpcModelSymbol
from openai import OpenAI

import os

OPEN_API_KEY = os.getenv('OPEN_API_KEY')
client = OpenAI(api_key=OPEN_API_KEY)





# Load SpaCy's NLP model
nlp = spacy.load("en_core_web_sm")


# OpenAIService class definition
class OpenAIService:
    @staticmethod
    def get_patent_ideas(description,creativity, engine="gpt-3.5-turbo-instruct"):
        prompt = f"Generate patentable scopes for: {description}"
        logging.info(f"Sending prompt to OpenAI: {prompt}")
        
        try:
            response = client.completions.create(model=engine, prompt=prompt, max_tokens=200,temperature=creativity)
            scopes = response.choices[0].text.strip().split('\n')
            scopes = [scope for scope in scopes if len(scope) > 10]
            logging.info(f"Received patentable scopes from OpenAI: {scopes}")
            return scopes
        except Exception as e:
            logging.error(f"Error in get_patent_ideas: {e}")
            raise OpenAIError(f"Error in generating patent ideas: {e}")

    
   

# Define OpenAI Error class
class OpenAIError(Exception):
    pass

    
# Flask route to create a new patent
def create_patent2(description,creativity): 
    try:
        patent_description = description
        patentable_scopes = OpenAIService.get_patent_ideas(patent_description,creativity)

        print(patentable_scopes,'patentable_scopespatentable_scopespatentable_scopes')
        # Construct the URL
        patentable_scopes = "/".join(patentable_scopes)
        url = f'https://ipcpub.wipo.int/search/ipccat/20240101/en/subgroup/3/{patentable_scopes}/'

        # Make a request to the API
        response = requests.get(url)

        # Now you can work with the response object, for example, check the status code
        if response.status_code == 200:
            print('Request successful')
            print(response.text)
             # Parse the HTML response
            soup = BeautifulSoup(response.text, 'html.parser')
            a_tags = soup.select('div.srchres a')

            # Extract the values
            values = [(a.text.strip(), a['href'].split('/')[-2]) for a in a_tags]

            # Print the result
            ipc_symbols = []
            for value in values:
                ipc_symbols.append(value[1])
                print(f"Code: {value[1]}")      
            print(ipc_symbols,'----------------------------------ipc_symbols')    
            # Add further processing based on the API response
        else:
            print(f'Request failed with status code {response.status_code}')

        print('patent_description: ', patent_description)
        print('patentable_scopes: ', patentable_scopes)
        # print('ipc_symbols: ', ipc_symbols)

        ipc_objects = IpcModelSymbol.objects.filter(symbol__in=ipc_symbols)

        formatted_data = []
        for i in ipc_objects:

            if len(i.symbol) < 15:
            # Format main_class, main_group, and subgroup to ensure they are 2 characters long
                symbol = i.symbol + "0" * (15 - len(i.symbol))

            section = symbol[0:1]  # A63B
            main_class = symbol[1:3]  # 41
            subclass = symbol[3]  # /
            main_group = symbol[5:8]  # 12
            subgroup = symbol[8:10]  # 0000

            formatted_data.append({
                'section': section,
                'main_class': main_class,
                'subclass': subclass,
                'main_group': main_group,
                'subgroup': subgroup,
                'ipc_object':{
                    "text_body": i.text_body,
                    "edition":i.edition
                }
            })
            

        return ipc_symbols, patentable_scopes,formatted_data
    except Exception as e:
        print(e)
    

def generate_confidentiality_notice(client_company_name):
        prompt = f"Generate a confidentiality notice emphasizing the importance of the information's privacy and restricted use within a patent analysis report for {client_company_name}."
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=240
        )
        market_overview = response.choices[0].text.strip()
        return market_overview


def generate_executive_summary(get_patent_title):
        prompt = f"Provide a high-level overview summarizing the novel features and market impact of {get_patent_title} described above."
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=250
        )
        market_overview = response.choices[0].text.strip()
        return market_overview

# create_patent()