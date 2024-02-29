import fitz
import base64
from .models import IpcModelSymbol
from bs4 import BeautifulSoup
from openai import OpenAIError
from openai import OpenAI


import os

OPEN_API_KEY = os.getenv('OPEN_API_KEY')
client = OpenAI(api_key=OPEN_API_KEY)

def save_all_pages_as_png(pdf_path: str, output_folder: str):
    pdf_document = fitz.open(pdf_path)
    image_paths = []

    for page_number in range(pdf_document.page_count):
        # Load each page
        current_page = pdf_document.load_page(page_number)
        
        # Get a pixmap for the page
        pixmap = current_page.get_pixmap()

        # Save the pixmap as a PNG image
        image_path = f"{output_folder}/page_{page_number + 1}.png"
        pixmap.save(image_path)

        # Append the image path to the list
        image_paths.append(image_path)

    pdf_document.close()

    # Return the list of image paths
    return image_paths

# Example usage
# pdf_path = "/home/toshar/Documents/mukesh docss/IPC PROJECT/ipc_project/ipc/US20240009542A1.pdf"
# pdf_path = '/home/toshar/Documents/mukesh docss/IPC PROJECT/ipc_project/ipc/EP2127518B1.pdf'
# output_folder = '/home/toshar/Documents/mukesh docss/IPC PROJECT/ipc_project/pdf_uploads'
# images = save_all_pages_as_png(pdf_path, output_folder)

# Print the list of image paths
# print(images, '-------images')

import base64

def encode_image(image_path: str):
    new_data = []

    for image in image_path:
        with open(image, 'rb') as image_file:
            # Read the binary content of the image file
            binary_data = image_file.read()

            # Encode the binary data in base64
            base64_encoded = base64.b64encode(binary_data)

            # Decode the bytes to a UTF-8 string and append to the list
            new_data.append(base64_encoded.decode('utf-8'))

    return new_data

# Process each image individually
# new_data = []
# for image_path in images:
#     data = encode_image(image_path)
#     new_data.append(data)
    # print(data,'=========================')

import requests
import json

OPEN_API_KEY = os.getenv('OPEN_API_KEY')
client = OpenAI(api_key=OPEN_API_KEY)

def call_gpt4_with_image(new_data):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPEN_API_KEY}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "provide precise summary of 6-7 lines for the text or data"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{new_data}",
                            "detail": "low"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response

# data = call_gpt4_with_image(new_data)
# data = json.loads(data.text)
# print(data,'090909090909----------------------------')
# data = data['choices'][0]['message']['content']
# print(data,'[[[[[[[]]]]]]]')



# openai.api_key = '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'


class OpenAIService:
    @staticmethod
    def get_patent_ideas(data, engine="gpt-3.5-turbo-instruct"):
        prompt = f"Generate patentable scopes for: {data}"
      
        
        try:
            response = client.completions.create(model=engine, prompt=prompt, max_tokens=150)
            scopes = response.choices[0].text.strip().split('\n')
            scopes = [scope for scope in scopes if len(scope) > 10]
            
            return scopes
        except Exception as e:
            raise OpenAIError(f"Error in generating patent ideas: {e}")
        
# data=OpenAIService.get_patent_ideas(data)
# print(data,'pppppp------------------')


def create_patent_pdf_images(data): 
    # print(data,'beforegptttttttt-------------------------')
    
    try:
        patentable_scopes = OpenAIService.get_patent_ideas(data) 
      
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