from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.coronavstech.companies.models import Company
from api.coronavstech.companies.serializers import CompanySerializer


# Create your views here.
class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination

# @api_view(http_method_names=["POST"])
# def send_company_email(request):
#
#     send_mail(subject="My cool subject", message="My cool message",
#               from_email="test@test.com",
#               recipient_list=["dahun4032@gmail.com"]
#               )
#     return Response({"status":"success", "info":"email sent successfully."}, status=200)
