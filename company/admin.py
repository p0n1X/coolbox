from django.contrib import admin
from .models import Company, CompanyDetails, FinancialData

admin.site.register(Company)
admin.site.register(CompanyDetails)
admin.site.register(FinancialData)