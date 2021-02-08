from django.shortcuts import render
from .models import FAQQuestion
from .serializers import (
    GetQuestionSerializer, GetSmallQuestionSerializer
) 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from learnpack.utils import ValidationException

class FAQQuestionView(APIView):

    permission_classes = [AllowAny]
    def get(self, request, slug=None, lang='us'):
        if slug is not None:
            question = FAQQuestion.objects.filter(slug=slug, language=lang).first()
            if question is None:
                raise ValidationException(f"Question not found on language {lang}", 404)
            else:
                serializer = GetQuestionSerializer(question, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)

        query = FAQQuestion.objects.all()

        lang = request.GET.get('lang', '')
        if lang != '':
            lang = query.filter(lang=lang)

        _status = request.GET.get('status', '')
        if _status == '':
            _status = 'PUBLISHED'
        query = query.filter(status=_status)
        query = query.order_by('-priority')


        serializer = GetSmallQuestionSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)