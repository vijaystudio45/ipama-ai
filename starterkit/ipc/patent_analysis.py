# backend\patent_analysis.py

import json
from openai import OpenAI

import logging
import os
from datetime import datetime
import spacy
from fuzzywuzzy import fuzz
from collections import defaultdict
import requests
from .models import IpcModelSymbol
# from openai import OpenAI



import os

OPEN_API_KEY = os.getenv('OPEN_API_KEY')
client = OpenAI(api_key=OPEN_API_KEY)
# Load SpaCy's NLP model
nlp = spacy.load("en_core_web_sm")

# Load IPC data from file
# ipc_data_file_path = os.path.join(os.path.dirname(__file__), 'WIPO', 'IPC', 'ipc_data.json')
# ipc_data_file_path = '/home/toshar/Documents/mukesh docss/IPC PROJECT/ipc_project/ipc/ipc_data.json'
# try:
#     with open(ipc_data_file_path, 'r', encoding='utf-8') as f:
#         ipc_data = json.load(f)
#     logging.info(f"Successfully loaded IPC data from {ipc_data_file_path}")
# except Exception as e:
#     ipc_data = {}
#     logging.error(f"Error loading IPC data: {e}")

# OpenAIService class definition
class OpenAIService:
    @staticmethod
    def get_patent_ideas(description, engine="gpt-3.5-turbo-instruct"):
        prompt = f"Generate patentable scopes for: {description}"
        logging.info(f"Sending prompt to OpenAI: {prompt}")
        
        try:
            response = client.completions.create(engine=engine, prompt=prompt, max_tokens=200)
            scopes = response.choices[0].text.strip().split('\n')
            scopes = [scope for scope in scopes if len(scope) > 10]
            logging.info(f"Received patentable scopes from OpenAI: {scopes}")
            return scopes
        except Exception as e:
            logging.error(f"Error in get_patent_ideas: {e}")
            raise OpenAIError(f"Error in generating patent ideas: {e}")


    # @staticmethod
    # def perform_patent_analysis(description):
    #     logging.info(f"Starting patent analysis for description: {description}")
    #     analysis_results = []
    #     def analyze_entries(entries, symbol_prefix=''):
    #         for entry in entries:
    #             symbol = symbol_prefix + entry['symbol']
    #             entry_text = entry.get('text', '').lower()
    #             logging.info(f"Analyzing IPC entry: {symbol}")

    #             if OpenAIService.is_relevant(entry_text, description):
    #                 analysis_results.append(symbol)
    #                 logging.info(f"Relevant IPC symbol found: {symbol} for text: {entry_text}")
    #             if 'sub_entries' in entry:
    #                 analyze_entries(entry['sub_entries'], symbol)
    #     try:
    #         analyze_entries(ipc_data)
    #         logging.info(f"Completed patent analysis. Results: {analysis_results}")
    #         return analysis_results
    #     except Exception as e:
    #         logging.error(f"Error in perform_patent_analysis: {e}")
    #         raise OpenAIError(f"Error in patent analysis: {e}")
    
    @staticmethod
    def is_relevant(entry_text, description):
        similarity_threshold = 60
        return fuzz.token_sort_ratio(entry_text, description) > similarity_threshold

    @staticmethod
    def similarity(text1, text2):
        return fuzz.token_sort_ratio(text1, text2)

# Define OpenAI Error class
class OpenAIError(Exception):
    pass

# Utility functions
def extract_keywords(text):
    logging.info(f"Extracting keywords from text: {text}")
    doc = nlp(text)
    return [token.lemma_ for token in doc if token.pos_ in ['NOUN', 'PROPN']]

def calculate_similarity_score(ipc_text, keyword):
    logging.info(f"Calculating similarity score between IPC text and keyword: {keyword}")
    return fuzz.token_sort_ratio(ipc_text, keyword)

import ast
from django.db.models import Q

# Main function to find best matching IPC symbol
def find_best_matching_ipc_symbol(scope_description, ipc_entries):
    logging.info(f"Finding best matching IPC symbol for scope: {scope_description}")
    keywords = extract_keywords(scope_description)
    try:
        query = Q()
        for keyword in keywords:
            query |= Q(text_body__icontains=keyword)

        ipc_entries = ipc_entries.filter(query)
        best_matches_per_keyword = defaultdict(lambda: {'symbol': None, 'score': 0})
    except Exception as e:
        print(e, "LLLLLLLLLLLLLLLLLLLLLLLLLLL")

    def recursive_search(entries, path=[]):
        for entry in entries:
            # current_path = path + [entry['symbol']] # A
            current_path = entry.symbol # A
            entry_text = ' | '.join(filter(lambda x: x is not None, ast.literal_eval(entry.text_body)))

            # print(keywords, "::::::::::_----------",entry_text)
            for keyword in keywords:
                similarity_score = calculate_similarity_score(entry_text, keyword)
                logging.debug(f"Checking IPC entry {' > '.join(current_path)} with keyword '{keyword}' and similarity score: {similarity_score}")

                if similarity_score > best_matches_per_keyword[keyword]['score']:
                    best_matches_per_keyword[keyword] = {'symbol': entry.symbol, 'score': similarity_score}
                    logging.info(f"New best match for keyword '{keyword}': {entry.symbol} with score: {similarity_score}")

            # if 'sub_entries' in entry:
            #     recursive_search(entry['sub_entries'], current_path)
    recursive_search(ipc_entries)

    overall_best_match = max(best_matches_per_keyword.values(), key=lambda x: x['score'])
    if overall_best_match['symbol']:
        logging.info(f"Best matching IPC symbol found: {overall_best_match['symbol']}")
        return overall_best_match['symbol'], "Matching text for best match"  # Placeholder for actual logic
    else:
        logging.warning("No matching IPC symbol found.")
        return None, None
    
# Flask route to create a new patent
def create_patent_data(description):

    try:
        patent_description = description
        logging.info("Generating patentable scopes and matching IPC symbols.")
        patentable_scopes = OpenAIService.get_patent_ideas(patent_description)
        ipc_symbols = match_scopes_to_ipc_symbols(patentable_scopes)

        # print('patent_description: ', patent_description)
        # print('patentable_scopes: ', patentable_scopes)
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
                'ipc_object':i
            })
            

        return ipc_symbols, patentable_scopes,formatted_data
    except Exception as e:
        print(e)
    

# Function to match patent scopes to IPC symbols
def match_scopes_to_ipc_symbols(patentable_scopes):
    logging.info("Matching patentable scopes to IPC symbols.")
    matched_symbols = []
    for scope in patentable_scopes:
        if scope:
            try:
                ipc_data2 = IpcModelSymbol.objects.all()
                matched_symbol, matched_text = find_best_matching_ipc_symbol(scope, ipc_data2)
                if matched_symbol:
                    logging.info(f"Scope: {scope} - Matched IPC Symbol: {matched_symbol} with text: '{matched_text}'")
                    matched_symbols.append(matched_symbol)
                else:
                    logging.warning(f"Scope: {scope} - No matching IPC Symbol found.")
            except Exception as e:
                logging.error(f"Error matching IPC symbol for scope '{scope}': {e}")
                matched_symbols.append("Error in matching")
    return matched_symbols


# create_patent()