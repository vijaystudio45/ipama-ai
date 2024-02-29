#for questioning pdf we have used this functionality.

from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
# from langchain_openai import OpenAI
import os
from langchain_community.llms.openai import OpenAI
import fitz  # PyMuPDF
from pdf2image import convert_from_path
from pytesseract import image_to_string



import os

OPEN_API_KEY = os.getenv('OPEN_API_KEY')
client = OpenAI(api_key=OPEN_API_KEY)
# os.environ['open_api_key'] = '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'


# document_path = '/home/studio/Documents/py projects/starterkit/ipc/US10212857.pdf'


def questioning_pdf_for_data(document_path):
    # pdfreader = PdfReader(document_path)
    # raw_text = ''
    # for i, page in enumerate(pdfreader.pages):
    #     content = page.extract_text()
    #     if content:
    #         raw_text += content
    raw_text = ''
    doc = fitz.open(document_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        raw_text += text

    doc.close()

  
    if not raw_text:
        # Use PyPDF2 to extract text from image-based PDF
        pdfreader = PdfReader(document_path)
        raw_text = ''
        for i, page in enumerate(pdfreader.pages):
            # Convert each page to an image and extract text using pytesseract
            images = convert_from_path(document_path, first_page=i + 1, last_page=i + 1)
            for img in images:
                img_text = image_to_string(img, lang='eng')
                raw_text += img_text


    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1800, chunk_overlap=200, length_function=len)
    texts = text_splitter.split_text(raw_text)
 
    embeddings = OpenAIEmbeddings(openai_api_key=OPEN_API_KEY)
    print(embeddings,'p-p-p-p-p-p-p-embeddingsssss')

    document_search = FAISS.from_texts(texts, embeddings)
    # print(document_search,'------document_search-----')
    chain = load_qa_chain(OpenAI(openai_api_key=OPEN_API_KEY), chain_type='stuff')
    # query = "who is Inventor in this pdf?"
    queries = ["who is the Inventor in this pdf?", "what will be the main topic of this pdf written in bold letters?","What is the publication date in this pdf?","what is the Abstract in this pdf","what is the field of invention in this pdf?, what is the Application date or Publication date in this pdf?"]

    pdf_data_response = {}
    for query in queries:
        docs = document_search.similarity_search(query)
        # print(docs,'----docs------')
        data = chain.run(input_documents=docs, question=query)
        # print(data, '---------dadada')
        if "Inventor" in query:
            pdf_data_response['inventor'] = data
        elif "main_topic" in query:
            pdf_data_response['main_topic'] = data
        # elif "Summary" in query:
        #     pdf_data_response['Summary'] = data
        elif "Abstract" in query:
            pdf_data_response['Abstract'] = data
        elif "field of invention" in query:
            pdf_data_response['field_of_invention'] = data
        elif "Application or Publication" in query:
            pdf_data_response['Application_date'] = data

    return pdf_data_response