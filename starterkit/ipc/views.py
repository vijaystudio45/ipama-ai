from django.shortcuts import render
# Create your views here.
import json
import xmltodict
from django.http import HttpResponse, JsonResponse,HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from .forms import UploadFileForm,PdfFileUploadForm
from .read_xml import read_xml_file  # Replace with your actual form
# from .models import UploadedFile  # Replace with your actual model
from .models import IpcModelSymbol
from django.views.generic import ListView
import openai
from .forms import PatentForm  
from django.shortcuts import render, redirect
from .patent_analysis import create_patent_data
from .patent_search_api import generate_confidentiality_notice,create_patent2,generate_executive_summary
from django.views.generic import TemplateView
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from .models import Patent
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django_countries import countries as django_countries_list




class UploadAndConvertView(LoginRequiredMixin,TemplateView):
    template_name = 'pages/ipc/upload_and_convert_file.html'
    # layout_template = 'auth.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['form'] = UploadFileForm()
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        return context


    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            uploaded_file = form.save()
            read_xml_file(uploaded_file.file)
            context['message'] = f"{uploaded_file.file.name} file is uploaded successfully"
            return JsonResponse(context,status=200)
        else:
            context['message'] = f"Something Went Wrong Please Upload Different File"
            return JsonResponse(context,status=400)

        
       



class IpcModelSymbolListView(LoginRequiredMixin,ListView):
    model = IpcModelSymbol
    template_name = 'ipc_list.html'  # Replace with the actual template name
    context_object_name = 'symbols'

    def get_queryset(self):
        # Retrieve the query parameters from the request
        symbol = self.request.GET.get('symbol', None)
        text_body = self.request.GET.get('text_body', None)

        # Filter the queryset based on the parameters
        # del_old_data = IpcModelSymbol.objects.all().delete()
        queryset1 = IpcModelSymbol.objects.all()
        queryset = []
        if symbol:
            queryset = queryset1.filter(symbol=symbol)
        if text_body:
            queryset = queryset1.filter(text_body__icontains=text_body)


        return queryset
    





class create_patentView(LoginRequiredMixin,TemplateView):
    template_name = 'pages/ipc/create_patent.html'


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)
        # Include vendors and javascript files for dashboard widgets
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        context['countries'] = [(country_code, country_name) for country_code, country_name in django_countries_list]
        return context


    def post(self, request, *args, **kwargs):
        form = PatentForm(request.POST)
        if form.is_valid():
            # form.save()
            creativity = float(request.POST.get('creativity_range'))
            patent_description = form.cleaned_data.get('patent_description')
            client_company_name = form.cleaned_data.get("client_company_name")
            get_patent_title = form.cleaned_data.get("patent_title")
            generate_confidentiality = generate_confidentiality_notice(client_company_name)
            generate_summary = generate_executive_summary(get_patent_title)
            symbols, patentable_scopes, formatt = create_patent2(patent_description,creativity)
            print(generate_summary,'------------------------------')
            context = {
                "ipc_objects": formatt,
                "patentable_scopes": patentable_scopes,
                "client_company_name":form.cleaned_data.get('client_company_name'),
                "client_contact_info":form.cleaned_data.get('client_contact_info'),
                "country_origin":form.cleaned_data.get('country_origin'),
                "country_filing_destination":form.cleaned_data.get('country_filing_destination'),
                "confidentiality_notice":generate_confidentiality,
                "generate_summary":generate_summary
            }

            for i in formatt:
                patent_instance = Patent.objects.create(
                        patent_title=form.cleaned_data.get('patent_title'),
                        patent_owner=form.cleaned_data.get('patent_owner'),
                        patent_description=patent_description,
                        patent_date=form.cleaned_data.get('patent_date'),
                        client_company_name=form.cleaned_data.get('client_company_name'),
                        client_contact_info=form.cleaned_data.get('client_contact_info'),
                        country_origin=form.cleaned_data.get('country_origin'),
                        country_filing_destination=form.cleaned_data.get('country_filing_destination'),
                        # patentable_scopes=patentable_scopes,
                        # ipc_symbols=symbols,
                        Scopes=patentable_scopes,
                        cip_Edition='',
                        cip_Section=i['section'],
                        cip_class=i['main_class'],
                        cip_ubclass=i['subclass'],
                        cip_Group=i['main_group'],
                        cip_Subgroup=i['subgroup'],
                        Description=i['ipc_object']['text_body'],
                        user=request.user  # Assuming you have the user available in the request
                    )
                # You can then save this instance to the database if needed:
                patent_instance.save()
            return JsonResponse({'success': True, 'context': context})
        else:
            return JsonResponse({'error': True, 'context': 'Please fill all the details'})
        


class Upload_HistoryView(LoginRequiredMixin,TemplateView):
    template_name = 'pages/ipc/patent_history.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        patient = Patent.objects.filter(user=self.request.user)
        context['patient'] = patient
        # Include vendors and javascript files for dashboard widgets
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        return context
    



class HistoryDetailView(DetailView):
    model = Patent
    template_name = 'pages/ipc/patent_history.html'  # You can create an empty template or use a different one if needed

    def render_to_response(self, context, **response_kwargs):
        # Customize the JsonResponse as needed
        data = {
            'id': self.object.id,
            'Scopes': self.object.Scopes,
            'cip_Section': self.object.cip_Section,
            'cip_Edition': self.object.cip_Edition,
            'cip_class': self.object.cip_class,
            'cip_ubclass': self.object.cip_ubclass,
            'cip_Group': self.object.cip_Subgroup,
            'Description': self.object.Description,
            # Add other fields you want to include in the JSON response
        }
        return JsonResponse(data)
    



class QuestionandanswerView(LoginRequiredMixin,TemplateView):
    template_name = 'pages/ipc/mainQuestion.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        # Include vendors and javascript files for dashboard widgets
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        return context
    

class QuestionView(LoginRequiredMixin,TemplateView):
    template_name = 'pages/ipc/QuestionAndAnswer.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        # Include vendors and javascript files for dashboard widgets
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        context['countries'] = [(country_code, country_name) for country_code, country_name in django_countries_list]
        return context
# class HistoryDetailView(LoginRequiredMixin,TemplateView):
#     template_name = 'pages/ipc/patent_history.html'

#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         context = KTLayout.init(context)

#         patient = Patent.objects.filter(user=self.request.user)
#         context['patient'] = patient
#         # Include vendors and javascript files for dashboard widgets
#         KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
#         return context





##-------this code is to read the text from pdf---------##

# from .pdf_reader import create_patent_pdf,get_pdf_text,summarize_data
# from django.forms.models import model_to_dict


# class UploadPdfView(LoginRequiredMixin,TemplateView):
#     template_name = 'pages/ipc/upload_pdf_and_convert_file.html'
#     # layout_template = 'auth.html'

#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         context = KTLayout.init(context)
#         context['form'] = UploadFileForm()
#         KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
#         return context
    

#     def post(self, request, *args, **kwargs):
#         message = None

#         # if request.method == 'POST':
#         form = PdfFileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#                 uploaded_file = form.cleaned_data['file']
            
#                 # Check if the uploaded file has a PDF format
#                 if not uploaded_file.name.lower().endswith('.pdf'):
#                     return HttpResponseBadRequest("Only PDF files are allowed.")
#                 uploaded_file = form.save()
#                 # print(uploaded_file.file)
#                 pdf_text=get_pdf_text(uploaded_file.file)
#                 summarize_all_data = summarize_data(pdf_text)
#                 ipc_symbols, patentable_scopes,formatted_data = create_patent_pdf(summarize_all_data)
#                 # Process the uploaded PDF file
#                 # process_pdf(uploaded_file.file.path)
#                 formatted_data_json = []
#                 for i in formatted_data:
#                     if len(i['ipc_object'].symbol) < 15:
#                         # Format main_class, main_group, and subgroup to ensure they are 2 characters long
#                         symbol = i['ipc_object'].symbol + "0" * (15 - len(i['ipc_object'].symbol))

#                         section = symbol[0:1]  # A63B
#                         main_class = symbol[1:3]  # 41
#                         subclass = symbol[3]  # /
#                         main_group = symbol[5:8]  # 12
#                         subgroup = symbol[8:10]  # 0000

#                         formatted_data_json.append({
#                             'section': section,
#                             'main_class': main_class,
#                             'subclass': subclass,
#                             'main_group': main_group,
#                             'subgroup': subgroup,
#                             'text_body': i['ipc_object'].text_body,
#                             'ipc_object': str(i['ipc_object'])  # Assuming you want to store the string representation
#                         })

#                 context = {
#                     "ipc_objects": formatted_data_json,
#                     "patentable_scopes": patentable_scopes,
#                 }

#                 # return render(request,'pdf_data_ipc.html',{'form': form,'context':context})
#                 return JsonResponse({'success': True, 'context': context})
                
#         else:
#             # form = PdfFileUploadForm()
#             return JsonResponse({'error': True, 'context': 'Please upload correct pdf file.'})
            


#upload pdf with images and gerenate scopes 
from .image_read_pdf import save_all_pages_as_png,encode_image,call_gpt4_with_image,OpenAIService,create_patent_pdf_images
import os
from datetime import datetime
from .questioning_pdf_data import questioning_pdf_for_data
from .pdf_dataset import OpenAIServiceForPdf


class pdf_file_upload_with_imagesview(LoginRequiredMixin,TemplateView):
    template_name = 'pages/ipc/upload_pdf_and_convert_file.html'
    # layout_template = 'auth.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['form'] = UploadFileForm()
        context['countries'] = [(country_code, country_name) for country_code, country_name in django_countries_list]
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])

        return context

    def post(self,request, *args, **kwargs):
        message = None

        form = PdfFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
                uploaded_file = form.cleaned_data['file']
                company_name = form.cleaned_data['client_company_name']
                print(company_name,'=-=-=-=-=-=-=-=-company_name')
            
                # Check if the uploaded file has a PDF format
                if not uploaded_file.name.lower().endswith('.pdf'):
                    return HttpResponseBadRequest("Only PDF files are allowed.")
                uploaded_file = form.save()
                # print(uploaded_file.file)
                current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                user_specific_folder = f"pdf_uploads/pdf_images/user_{current_datetime}"
                file_path = os.mkdir(user_specific_folder)
                # print(file_path,'--------filepath')

                generate_confidentiality = OpenAIServiceForPdf.generate_confidentiality_notice(company_name)
                save_pdf_pages=save_all_pages_as_png(uploaded_file.file,user_specific_folder)
                image_path=encode_image(save_pdf_pages)
                new_data=call_gpt4_with_image(image_path)
                data = json.loads(new_data.text)
                print(data,'--------choicesssss')
                data = data['choices'][0]['message']['content']
                # data=OpenAIService.get_patent_ideas(data)
                ipc_symbols, patentable_scopes,formatted_data = create_patent_pdf_images(data)
                
                data_from_pdf = questioning_pdf_for_data(str(uploaded_file.file))
                print(data_from_pdf, '-0-0-data_from_pdf-0-0-')
                # print(data_from_pdf,'-9999999---')
                additional_generated_pdf_data = OpenAIServiceForPdf.get_patent_ideas_pdf(ipc_symbols)
                # print(additional_generated_pdf_data,'ppppppadditional_generated_pdf_dataadditional_generated_pdf_data')
                market_overview = OpenAIServiceForPdf.generate_market_overview(data_from_pdf['field_of_invention'])
                generate_innovative_component = OpenAIServiceForPdf.generate_innovative_component(
                    data_from_pdf['field_of_invention'])
                generate_potential_application = OpenAIServiceForPdf.generate_potential_application(
                    data_from_pdf['field_of_invention'])
                ip_protection_strategies = OpenAIServiceForPdf.ip_protection_strategies(data_from_pdf['field_of_invention'])
                licensing_opportunities = OpenAIServiceForPdf.licensing_opportunities(data_from_pdf['field_of_invention'])
                future_directions = OpenAIServiceForPdf.future_directions(data_from_pdf['field_of_invention'])
                collaboration_opportunities = OpenAIServiceForPdf.collaboration_opportunities(
                    data_from_pdf['field_of_invention'])
                glossary_terms = OpenAIServiceForPdf.glossary_terms(data_from_pdf['field_of_invention'])
                target_market_segments = OpenAIServiceForPdf.target_market_segments(data_from_pdf['field_of_invention'])
                enhanced_ipc_analysis = OpenAIServiceForPdf.enhanced_ipc_analysis(data_from_pdf['field_of_invention'])
                regulatory_landscape=OpenAIServiceForPdf.regulatory_landscape(data_from_pdf['field_of_invention'])
                compliance_requirements=OpenAIServiceForPdf.compliance_requirements(data_from_pdf['field_of_invention'])
                abstract = OpenAIServiceForPdf.abstract(data_from_pdf['field_of_invention'])
                reference = OpenAIServiceForPdf.reference(data_from_pdf['field_of_invention'])
                summary = OpenAIServiceForPdf.generate_executive_summary(data_from_pdf['field_of_invention'])
                # graphs = OpenAIServiceForPdf.interactive_graphs(data_from_pdf['field_of_invention'])
                # print(graphs)


                formatted_data_json = []
                for i in formatted_data:
                        print(1)
                    # if len(i['ipc_object'].symbol) < 15:
                    #     # Format main_class, main_group, and subgroup to ensure they are 2 characters long
                    #     symbol = i['ipc_object'].symbol + "0" * (15 - len(i['ipc_object'].symbol))

                        section = i['section']  # A63B
                        main_class = i['main_class']  # 41
                        subclass = i['subclass']  # /
                        main_group = i['main_group']  # 12
                        subgroup = i['subgroup']  # 0000

                        formatted_data_json.append({
                            'section': section,
                            'main_class': main_class,
                            'subclass': subclass,
                            'main_group': main_group,
                            'subgroup': subgroup,
                            'text_body': i['ipc_object'].text_body,
                            'ipc_object': str(i['ipc_object'])  # Assuming you want to store the string representation
                        })
                # print(formatted_data_json,'-------formatted_data_json') 

                context = {
                    "client_company_name":form.cleaned_data.get('client_company_name'),
                    "client_contact_info":form.cleaned_data.get('client_contact_info'),
                    "country_origin":form.cleaned_data.get('country_origin'),
                    "country_filing_destination":form.cleaned_data.get('country_filing_destination'),
                    "ipc_objects": formatted_data_json,
                    "patentable_scopes": patentable_scopes,
                    "data_from_pdf": data_from_pdf,
                    "additional_generated_pdf_data": additional_generated_pdf_data,
                    "market_overview": market_overview,
                    "innovative_component": generate_innovative_component,
                    "generate_potential_application": generate_potential_application,
                    "ip_protection_strategies": ip_protection_strategies,
                    "licensing_opportunities": licensing_opportunities,
                    "future_directions": future_directions,
                    "collaboration_opportunities":collaboration_opportunities,
                    "glossary_of_terms":glossary_terms,
                    'target_market_segments':target_market_segments,
                    'enhanced_ipc_analysis':enhanced_ipc_analysis,
                    'regulatory_landscape':regulatory_landscape,
                    'compliance_requirements':compliance_requirements,
                    'Abstract':abstract,
                    'reference_and_links':reference,
                    'generate_confidentiality':generate_confidentiality,
                    'summary':summary
                    # 'graphs':graphs
                }

                return JsonResponse({'success': True, 'context': context})
        else:
            return JsonResponse({'error': True, 'context': 'Something went wrong.'})
        


# # this is to check user is admin or not
# class admin_View(LoginRequiredMixin, TemplateView):
#     # template_name = 'layout/partials/sidebar-layout/sidebar/menu.html'
#     template_name = 'pages/auth/signin.html'

#     # layout_template = 'auth.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Assuming KTLayout and KTTheme are defined somewhere else
#         context = KTLayout.init(context)
#         KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
#         # Add is_admin to context
#         is_admin = self.request.user.is_authenticated and self.request.user.is_superuser and self.request.user.is_staff
#         print(is_admin,'==========')
#         context['is_admin'] = is_admin

#         return context
        

        
