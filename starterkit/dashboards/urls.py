from django.urls import path
from django.conf import settings
from dashboards.views import DashboardsView,LandingPageView

app_name = 'dashboards'

urlpatterns = [
    path('', LandingPageView.as_view(template_name = 'pages/dashboards/landingpage.html'), name='landingpage'),
    path('dashboard/', DashboardsView.as_view(template_name = 'pages/dashboards/index.html'), name='index'),
    # path('test', DashboardsView.as_view(template_name = 'pages/dashboards/test.html'), name='test'),

    path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]