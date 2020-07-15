from django.shortcuts import render
from .models import Package, Technology, Language
from .serializers import GetPackageSerializer, GetTechnologySerializer, GetLanguageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, exceptions

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

    if request.GET.get('language'):
        query = query.filter(language=request.GET['language'])

    if request.GET.get('technology'):
        query = query.filter(technology=request.GET['technology'])

    serializer = GetPackageSerializer(query, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_by_slug(request, slug):
    package = Package.objects.filter(slug=slug).first()
    if package is None:
        raise exceptions.NotFound(detail="Package not found", code=status.HTTP_404_NOT_FOUND)
    serializer = GetPackageSerializer(package, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)