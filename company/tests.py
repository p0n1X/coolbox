from django.test import TestCase
from .services import CompanyServices

class CompanyTest(TestCase):
    def setUp(self):
        self.companies = [
            {"name": "Laptop BG", "country": "Bulgaria", "industry": "Technology", "founded_year": 2008,
             "company_type": "Public", "size": 250, "ceo_name": "Ivan Ivanov", "headquarters": "Plovdiv",
             "year": 2025, "revenue": 5000, "net_income": 3000},
            {"name": "SoftUni", "country": "Bulgaria", "industry": "Education", "founded_year": 2013,
             "company_type": "Private", "size": 500, "ceo_name": "Svetlin Nakov", "headquarters": "Sofia",
             "year": 2025, "revenue": 8000, "net_income": 2500},
            {"name": "SiteGround", "country": "Bulgaria", "industry": "Technology", "founded_year": 2004,
             "company_type": "Private", "size": 1000, "ceo_name": "Tenko Nikolov", "headquarters": "Sofia",
             "year": 2025, "revenue": 70000, "net_income": 20000},
            {"name": "Coca-Cola HBC Bulgaria", "country": "Bulgaria", "industry": "Beverages", "founded_year": 1992,
             "company_type": "Public", "size": 1500, "ceo_name": "Svetoslav Atanasov", "headquarters": "Plovdiv",
             "year": 2025, "revenue": 120000, "net_income": 15000},
            {"name": "Aurubis Bulgaria", "country": "Bulgaria", "industry": "Mining & Metals", "founded_year": 1958,
             "company_type": "Private", "size": 800, "ceo_name": "Tim Kurth", "headquarters": "Pirdop", "year": 2025,
             "revenue": 200000, "net_income": 25000},
            {"name": "Sopharma", "country": "Bulgaria", "industry": "Pharmaceuticals", "founded_year": 1933,
             "company_type": "Public", "size": 2000, "ceo_name": "Ognian Donev", "headquarters": "Sofia",
             "year": 2025, "revenue": 90000, "net_income": 18000},
            {"name": "Bulgartransgaz", "country": "Bulgaria", "industry": "Energy", "founded_year": 2007,
             "company_type": "State-owned", "size": 700, "ceo_name": "Vladimir Malinov", "headquarters": "Sofia",
             "year": 2025, "revenue": 60000, "net_income": 10000}
        ]

    def test_partial_search(self):
        search_string_partial = 'Publ'
        company_result = CompanyServices.search(search_string_partial, self.companies)
        self.assertEquals(3, len(company_result))

        search_string_additional = 'Publ  size > 300'
        company_result_additional = CompanyServices.search(search_string_additional, self.companies)
        self.assertEquals(2, len(company_result_additional))

        search_string_triple = 'headquarters: Sofia Publ size > 300'
        company_result_triple = CompanyServices.search(search_string_triple, self.companies)
        self.assertEquals(1, len(company_result_triple))

    def test_normal_search(self):
        search_string = 'industry:Technology revenue>6000'
        company_result = CompanyServices.search(search_string, self.companies)
        self.assertEquals(1, len(company_result))

        search_string_eq = 'industry=Technology revenue>6000'
        company_result_eq = CompanyServices.search(search_string_eq, self.companies)
        self.assertEquals(1, len(company_result_eq))

    def test_normal_search_with_sort(self):
        search_string_asc = 'company_type = Public size=ASC'
        company_data = self.companies
        company_sort = self.companies
        self.assertEquals(company_data, company_sort)

        company_sort = CompanyServices.search(search_string_asc, company_sort)
        self.assertEquals(250, company_sort[0].get('size'))
        self.assertNotEquals(company_data, company_sort)

        search_string_desc = 'company_type = Public size=DESC'
        company_sort = CompanyServices.search(search_string_desc, company_sort)
        self.assertEquals(2000, company_sort[0].get('size'))
        self.assertNotEquals(company_data, company_sort)



    def test_filter(self):
        filter_string = "company_type = Private AND headquarters=Sofia"
        company_result = CompanyServices.filter(filter_string, self.companies)
        self.assertEquals(2, len(company_result))

        filter_string_not = "company_type = Private NOT headquarters=Sofia"
        company_result_not = CompanyServices.filter(filter_string_not, self.companies)
        self.assertEquals(1, len(company_result_not))


    def test_sort(self):
        sort_desc = 'size=DESC'
        company_data = self.companies
        company_sort = self.companies
        self.assertEquals(company_data, company_sort)

        company_sort = CompanyServices.sort(sort_desc, company_sort)
        self.assertEquals(2000, company_sort[0].get('size'))
        self.assertNotEquals(company_data, company_sort)

        sort_asc = 'size=ASC'
        company_sort = CompanyServices.sort(sort_asc, company_sort)
        self.assertEquals(250, company_sort[0].get('size'))
        self.assertNotEquals(company_data, company_sort)


