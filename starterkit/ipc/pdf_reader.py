from langchain.chains import AnalyzeDocumentChain
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import OpenAI
from PyPDF2 import PdfReader
from openai import OpenAI


import requests
from .models import IpcModelSymbol
from bs4 import BeautifulSoup

import os

OPEN_API_KEY = os.getenv('OPEN_API_KEY')
client = OpenAI(api_key=OPEN_API_KEY)
# from langchain_community.llms import OpenAI

# This function is reading PDF from the start page to final page
# given as input (if less pages exist, then it reads till this last page)
# document_path='/home/toshar/Documents/mukesh docss/IPC PROJECT/ipc_project/ipc/US10212857.pdf'
# document_path = '/home/toshar/Documents/mukesh docss/IPC PROJECT/ipc_project/ipc/US20240009542A1.pdf'
def get_pdf_text(document_path, start_page=1, final_page=999):
    reader = PdfReader(document_path)
    number_of_pages = len(reader.pages)
    page=''
    for page_num in range(start_page - 1, min(number_of_pages, final_page)):
        page += reader.pages[page_num].extract_text()
   
    return page
# data = get_pdf_text(document_path)
# print(data,'ppppp')
   
def summarize_data(data):
    # apikey='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'
    apikey = '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'   #new api key adn
    model = OpenAI(temperature=0,openai_api_key=apikey)
    summary_chain = load_summarize_chain(llm=model, chain_type='map_reduce')
    summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain)
    print('output(AnalyzeDocumentChain):', summarize_document_chain.run(data))
    summary_data = summarize_document_chain.run(data)

    return summary_data

class OpenAIError(Exception):
    pass
# openai.api_key = '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'
class OpenAIService:
    @staticmethod
    def get_patent_ideas(data, engine="gpt-3.5-turbo-instruct"):
        prompt = f"Generate patentable scopes for: {data}"
      
        
        try:
            response = client.completions.create(engine=engine, prompt=prompt, max_tokens=200)
            scopes = response.choices[0].text.strip().split('\n')
            scopes = [scope for scope in scopes if len(scope) > 10]
            
            return scopes
        except Exception as e:
            raise OpenAIError(f"Error in generating patent ideas: {e}")
        
# data=OpenAIService.get_patent_ideas(summary_data)
# print(data,'pppppp------------------')


def create_patent_pdf(data): 
    # print(data,'beforegptttttttt-------------------------')
    
    try:
        patentable_scopes = OpenAIService.get_patent_ideas(data)
        print(patentable_scopes,'--------------------------------------pdf wala patent--------') 
      
        # patentable_scopes = "/".join(data)
        url = f'https://ipcpub.wipo.int/search/ipccat/20240101/en/subgroup/3/{patentable_scopes}/'

        # Make a request to the API
        response = requests.get(url)

        ipc_symbols = []
        # Now you can work with the response object, for example, check the status code
        if response.status_code == 200:
            print('Request successful')
            # print(response.text)
            
    #         #  Parse the HTML response
            soup = BeautifulSoup(response.text, 'html.parser')
            a_tags = soup.select('div.srchres a')

            # Extract the values
            values = [(a.text.strip(), a['href'].split('/')[-2]) for a in a_tags]

            # Print the result
            
            for value in values:
                ipc_symbols.append(value[1])
                print(f"Code: {value[1]}")      
            # print(ipc_symbols,'----------------------------------ipc_symbols')    
            # Add further processing based on the API response
        else:
            print(f'Request failed with status code {response.status_code}')

        # # print('patent_description: ', patent_description)
        # # print('patentable_scopes: ', patentable_scopes)
        # # print('ipc_symbols: ', ipc_symbols)

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