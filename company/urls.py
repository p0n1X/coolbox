from django.urls import path
from . import views

app_name = 'company'

urlpatterns = [
    path('', views.CompanyAPI.as_view(), name='show_all')
]