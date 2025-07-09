from django.db import connection
import re
import operator

QUERY_OPERATORS = {
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
    '=': operator.eq,
    ':': operator.eq
}

STR_FIELD = ('name', 'country', 'industry', 'company_type', 'ceo_name', 'headquarters', 'partial')
INT_FIELD = ('size', 'revenue', 'net_income', 'year', 'founded_year')
SORT_KEY = ('ASC', 'DESC')

class CompanyServices:

    @staticmethod
    def get_companies() -> list:
        cursor = connection.cursor()
        cursor.execute('SELECT c.*, d.company_type, d.size, d.ceo_name, d.headquarters, f.year, f.revenue, f.net_income \
                        FROM company_company c \
                        JOIN company_companydetails d ON c.id = d.company_id \
                        JOIN company_financialdata f ON c.id = f.company_id')
        raw_columns = []
        for column in range(len(cursor.description)):
            raw_columns.append(cursor.description[column][0])

        tuple_columns = tuple(raw_columns)
        companies = [dict(zip(tuple_columns, row)) for row in cursor.fetchall()]

        return companies

    @staticmethod
    def get_result(query_params: dict) -> list:
        search_string = query_params.get('q', '')
        filter_string = query_params.get('filter', '')
        sort_string = query_params.get('sort', '')
        companies = CompanyServices.get_companies()

        if search_string:
            companies = CompanyServices.search(search_string, companies)

        if filter_string:
            companies = CompanyServices.filter(filter_string, companies)

        if sort_string:
            companies = CompanyServices.sort(sort_string, companies)

        return companies

    @classmethod
    def _parse_search_string(cls, search_string: str) -> list:
        search_queries = re.findall(r'\b(\w+)\s*(>=|<=|=|>|<|:)\s*(\w+)\b|\b(\w+)\b', search_string)

        search_queries_list = []

        for field, str_operator, value, partial_value in search_queries:
            if partial_value:
                field = 'partial'
                value = partial_value
                str_operator = operator.eq
            else:
                str_operator = QUERY_OPERATORS.get(str_operator)
            search_queries_list.append({'field': field, 'operator': str_operator, 'value': value})
        return search_queries_list

    @classmethod
    def _parse_filter_string(cls, filter_string: str) -> list:
        filter_split = re.findall(r'\b(\w+)\s*(>=|<=|=|>|<|:)\s*(\w+)\b|\b(AND|OR|NOT)\b\s*([^ANDORNOT]+)',
                                  filter_string)
        filter_queries_list = []

        for field, str_operator, value, logic_operator, condition in filter_split:
            if logic_operator and condition:
                conditions = re.findall(r'\b(\w+)\s*(>=|<=|=|>|<|:)\s*(\w+)\b', condition)
                for field_condition, str_operator_condition, value_condition in conditions:
                    filter_queries_list.append({'field': field_condition, 'operator': QUERY_OPERATORS.get(str_operator_condition),'value': value_condition, 'logic_operator': logic_operator})
            else:
                str_operator = QUERY_OPERATORS.get(str_operator)
                filter_queries_list.append({'field': field, 'operator': str_operator, 'value': value, 'logic_operator': ''})

        return filter_queries_list

    @classmethod
    def _parse_sort_string(cls, sort_string: str) -> dict:
        field, value = sort_string.split('=')
        return {'field': field.strip(), 'order': value.strip()}

    @classmethod
    def search(cls, search_string: str, companies: list) -> list:
        search_queries = cls._parse_search_string(search_string)
        search_result = []
        sort_string = {}
        for company in companies:
            match = []
            for query in search_queries:
                field = query['field']
                query_operator = query['operator']
                value = query['value']
                if field in INT_FIELD:
                    if value in SORT_KEY:
                        sort_string = f'{field}={value}'
                        continue
                    elif not query_operator(company[field], float(value)):
                        match.append(False)
                        continue
                elif field in STR_FIELD :
                    if 'partial' == field:
                        check_partial_is_exist = any(value.lower() in str(company_value).lower() for company_value in company.values())
                        match.append(check_partial_is_exist)
                        continue
                    elif value.lower() not in company[field].lower():
                        match.append(False)
                        continue

            if False not in match:
                search_result.append(company)

        if sort_string:
            search_result = cls.sort(sort_string, search_result)

        return search_result

    @classmethod
    def filter(cls, filter_string: str, companies: list) -> list:
        filter_queries = cls._parse_filter_string(filter_string)
        filter_result = []

        for company in companies:
            match = []
            for query in filter_queries:
                field = query['field']
                query_operator = query['operator']
                value = query['value']
                logic_operator = query['logic_operator']
                if 'NOT' in logic_operator:
                    if field in INT_FIELD and query_operator(float(company[field]), float(value)):
                        match.append(False)
                        continue
                    elif field in STR_FIELD and query_operator(company[field].lower(), value.lower()):
                        match.append(False)
                        continue
                elif field in INT_FIELD and not query_operator(company[field], float(value)):
                    match.append(False)
                    continue
                elif field in STR_FIELD and not query_operator(company[field].lower(), value.lower()):
                    match.append(False)
                    continue
            if False not in match:
                filter_result.append(company)

        return filter_result

    @classmethod
    def sort(cls, sort_string: str, companies: list) -> list:
        sort_criteria = cls._parse_sort_string(sort_string)
        sorted_companies = cls.merge_sort(companies, sort_criteria)

        return sorted_companies

    @classmethod
    def merge_sort(cls, companies: list, sort_criteria: dict) -> list:
        if len(companies) <= 1:
            return companies

        mid = len(companies) // 2
        sort_left_company = companies[:mid]
        sort_right_company = companies[mid:]

        sort_left_company = cls.merge_sort(sort_left_company, sort_criteria)
        sort_right_company = cls.merge_sort(sort_right_company, sort_criteria)

        return cls.merge(sort_left_company, sort_right_company, sort_criteria)

    @classmethod
    def merge(cls, sort_left_company: list, sort_right_company: list, sort_criteria: dict) -> list:
        companies = []
        left_idx, right_idx = 0, 0

        while left_idx < len(sort_left_company) and right_idx < len(sort_right_company):
            if 'ASC' in sort_criteria['order']:
                if sort_left_company[left_idx].get(sort_criteria['field']) < sort_right_company[right_idx].get(sort_criteria['field']):
                    companies.append(sort_left_company[left_idx])
                    left_idx += 1
                else:
                    companies.append(sort_right_company[right_idx])
                    right_idx += 1
            else:
                if sort_left_company[left_idx].get(sort_criteria['field']) > sort_right_company[right_idx].get(sort_criteria['field']):
                    companies.append(sort_left_company[left_idx])
                    left_idx += 1
                else:
                    companies.append(sort_right_company[right_idx])
                    right_idx += 1

        companies.extend(sort_left_company[left_idx:])
        companies.extend(sort_right_company[right_idx:])

        return companies
