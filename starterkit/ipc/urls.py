from django.urls import path
from .views import IpcModelSymbolListView,UploadAndConvertView,create_patentView,Upload_HistoryView,HistoryDetailView,pdf_file_upload_with_imagesview,QuestionandanswerView,QuestionView

urlpatterns = [
    path('upload-and-convert/', UploadAndConvertView.as_view(), name='upload-and-convert'),
    path('ipc-list-search/', IpcModelSymbolListView.as_view(), name='symbol-list'),
      # path('create_patent/', create_patent, name='create_patent'),
    path('create_patent/', create_patentView.as_view(), name='create_patent'),
    path('upload-history/', Upload_HistoryView.as_view(), name='upload_history'),
    path('history-detail/<int:pk>/', HistoryDetailView.as_view(), name='history-detail'),
    path('pdf-upload/', pdf_file_upload_with_imagesview.as_view(), name='pdf-upload'),
    path('question-answer/', QuestionandanswerView.as_view(), name='question-answer'), 
    path('question-option/', QuestionView.as_view(), name='question-option'), 

    # path('pdf-upload/', UploadPdfView.as_view(), name='pdf-upload'), 


    # Add other URL patterns as needed
]