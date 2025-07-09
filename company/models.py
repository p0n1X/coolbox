from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    industry = models.CharField(max_length=50, blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class CompanyDetails(models.Model):
    company_type = models.CharField(max_length=50, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    ceo_name = models.CharField(max_length=100, blank=True, null=True)
    headquarters = models.CharField(max_length=100, blank=True, null=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE, blank=False)

    class Meta:
        verbose_name_plural = "Company Details"

    def __str__(self):
        return self.company.name


class FinancialData(models.Model):
    year = models.IntegerField(blank=True, null=True)
    revenue = models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)
    net_income = models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.company.name + f' Year: {self.year}'






