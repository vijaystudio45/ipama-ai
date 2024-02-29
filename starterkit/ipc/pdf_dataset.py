#to get all the description data from the pdf this functions are used

from openai import OpenAIError
import openai
from openai import OpenAI

# openai.api_key = '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'
import os

OPEN_API_KEY = os.getenv('OPEN_API_KEY')
client = OpenAI(api_key=OPEN_API_KEY)


class OpenAIServiceForPdf:
    @staticmethod
    def get_patent_ideas_pdf(ipc_symbols, engine="gpt-3.5-turbo-instruct"):
        descriptions = {}
        for symbol in ipc_symbols:
            prompt = f"Explain in short lines the IPC symbol {ipc_symbols} in the context of patent classification."
            response = client.completions.create(model=engine, prompt=prompt, max_tokens=200)
            descriptions[symbol] = response.choices[0].text.strip()
        return descriptions

    def generate_market_overview(field_of_invention):
        prompt = f"Provide a market overview for the {field_of_invention} industry, including trends, size, and growth potential with this headings ."
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=700
        )
        market_overview = response.choices[0].text.strip()
        return market_overview


    def generate_innovative_component(field_of_invention):
        prompt = f"Provide Innovative Components for the {field_of_invention}."
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200
        )
        innovative_component = response.choices[0].text.strip()
        return innovative_component

    def generate_potential_application(field_of_invention):
        prompt = f"Provide Potential Components for the {field_of_invention}."
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200
        )
        potential_application = response.choices[0].text.strip()
        return potential_application

    def ip_protection_strategies(field_of_invention):
        prompt = f"Provide IP Protection Strategies for the {field_of_invention}."
        response =client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200
        )
        ipc_protection = response.choices[0].text.strip()
        return ipc_protection

    #
    def licensing_opportunities(field_of_invention):
        prompt = f"Provide Licensing Opportunities for the {field_of_invention}."
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200
        )
        licensing_opportunities = response.choices[0].text.strip()
        return licensing_opportunities

    def future_directions(field_of_invention):
        prompt = f"Provide Future R&D Directions for the {field_of_invention}."
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200
        )
        furure_opportunities = response.choices[0].text.strip()
        return furure_opportunities

    def collaboration_opportunities(field_of_invention):
        prompt = f"Provide Collaboration Opportunities for the {field_of_invention}."
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200
        )
        collab = response.choices[0].text.strip()
        return collab

    def glossary_terms(field_of_invention):
        prompt = f"Provide Glossary of Terms for the {field_of_invention}."
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200
        )
        terms = response.choices[0].text.strip()
        return terms
    
    def target_market_segments(field_of_invention):
        prompt = f"Provide Target Market Segments for the {field_of_invention}."
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=180
        )
        segments = response.choices[0].text.strip()
        return segments
    
    def enhanced_ipc_analysis(field_of_invention):
        prompt = f"Provide Enhanced IPC Analysis for the {field_of_invention}."
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200
        )
        analysis = response.choices[0].text.strip()
        return analysis

    def regulatory_landscape(field_of_invention):
        prompt = f"Provide Regulatory Landscape for the {field_of_invention}."
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200
        )
        landscape = response.choices[0].text.strip()
        return landscape

    def compliance_requirements(field_of_invention):
        prompt = f"Provide Compliance Requirements for the {field_of_invention}."
        response =client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200
        )
        compliance = response.choices[0].text.strip()
        return compliance

    def abstract(field_of_invention):
        prompt = f"Provide Abstract for the {field_of_invention}."
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=170
        )
        abstract = response.choices[0].text.strip()
        return abstract
    
    def reference(field_of_invention):
        prompt = f"Generate a list of authoritative references and bibliographic citations that support the analysis provided in the patent report for {field_of_invention}, ensuring sources are credible and current"
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200
        )
        reference = response.choices[0].text.strip()
        return reference

    def generate_confidentiality_notice(client_company_name):
        prompt = f"Generate a confidentiality notice emphasizing the importance of the information's privacy and restricted use within a patent analysis report for {client_company_name}."
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=240
        )
        market_overview = response.choices[0].text.strip()
        return market_overview
    

    def generate_executive_summary(field_of_invention):
        prompt = f"Provide a high-level overview summarizing the novel features and market impact of {field_of_invention} described."
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=250
        )
        market_overview = response.choices[0].text.strip()
        return market_overview
    
    
    # def interactive_graphs(field_of_invention):
    #     client = OpenAI(api_key=OPEN_API_KEY)

    #     image_urls = []

    #     for _ in range(2):  # Make two requests
    #         response = client.images.generate(
    #             model="dall-e-3",
    #             prompt=f" Plot chart links in response showcasing the knowledgable data on {field_of_invention}.",
    #             size="1024x1024",
    #             quality="standard",
    #             n=1,
    #         )

    #         image_urls.append(response.data[0].url)

    #     return image_urls

