from django.shortcuts import render
from .models import Package, Technology, Language
from .serializers import (
    GetPackageSerializer, GetTechnologySerializer, GetLanguageSerializer,
    PostPackageSerializer,
) 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions

class PackageView(APIView):
    def get(self, request, slug):
        package = Package.objects.filter(slug=slug).first()
        if package is None:
            raise exceptions.NotFound(detail="Package not found", code=status.HTTP_404_NOT_FOUND)
        serializer = GetPackageSerializer(package, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        package = Package.objects.filter(slug=slug).first()
        if package is None:
            raise exceptions.NotFound(detail="Package not found", code=status.HTTP_404_NOT_FOUND)

        serializer = PostPackageSerializer(package, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, slug):
        package = Package.objects.filter(slug=slug).first()
        if package is not None:
            raise exceptions.NotFound(detail="Package already exists", code=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_technologies(request):
    items = Technology.objects.all()
    serializer = GetTechnologySerializer(items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_languages(request):
    items = Language.objects.all()
    serializer = GetLanguageSerializer(items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_packages(request):
    query = Package.objects.all()

    if request.GET.get('language', None):
        query = query.filter(language=request.GET['language'])

    if request.GET.get('technology', None):
        query = query.filter(technology=request.GET['technology'])

    serializer = GetPackageSerializer(query, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)