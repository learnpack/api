from django.shortcuts import render
from .models import Package
from .serializers import GetPackageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def get_packages(request):
    packages = Package.objects.all()
    serializer = GetPackageSerializer(packages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)