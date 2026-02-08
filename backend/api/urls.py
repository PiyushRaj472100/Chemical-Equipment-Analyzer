from django.urls import path
from .views import (
    UploadCSVView, 
    SummaryView, 
    HistoryView,
    RegisterView,
    LoginView,
    GeneratePDFReportView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload/', UploadCSVView.as_view(), name='upload-csv'),
    path('summary/', SummaryView.as_view(), name='summary'),
    path('history/', HistoryView.as_view(), name='history'),
    path('generate-pdf/', GeneratePDFReportView.as_view(), name='generate-pdf'),
    path('generate-pdf/<int:dataset_id>/', GeneratePDFReportView.as_view(), name='generate-pdf-id'),
]