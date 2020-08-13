from django.shortcuts import render
from .models import Package, Technology, Language
from .serializers import (
    GetPackageSerializer, GetTechnologySerializer, GetLanguageSerializer,
    PostPackageSerializer,
) 
from rest_framework.decorators import api_view
from .pagination import HeaderLimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.contrib.auth.models import User, Group, AnonymousUser
from rest_framework.exceptions import APIException, ValidationError, PermissionDenied
from learnpack.email import send_email_message

class PackageView(APIView):
    def get(self, request, slug):
        package = Package.objects.filter(slug=slug).first()
        if package is None:
            raise exceptions.NotFound(detail="Package not found", code=status.HTTP_404_NOT_FOUND)
        if not request.user.is_authenticated:
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

    

class UnspecifiedPackageView(APIView, HeaderLimitOffsetPagination):
    def get(self, request):
        query = Package.objects.exclude(private=True)
        if request.user.is_authenticated:
            query = Package.objects.all()
        if request.GET.get('language', None):
            query = query.filter(language=request.GET['language'])
        if request.GET.get('technology', None):
            query = query.filter(technology=request.GET['technology'])
        paginator = HeaderLimitOffsetPagination()
        page = paginator.paginate_queryset(query, request)
        print("PAGE: ", page)
        serializer = GetPackageSerializer(page, many=True)
        if page is not None:
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PostPackageSerializer(data=request.data, context = {"request": request})
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

