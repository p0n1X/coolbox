from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import CompanyServices


class CompanyAPI(APIView):
    def get(self, request):
        companies = CompanyServices.get_result(request.query_params)
        return Response(data=companies, status=status.HTTP_200_OK)