import serpy
from .models import FAQQuestion
from rest_framework import serializers
from learnpack.email import send_email_message
from learnpack.utils import ValidationException

class GetSmallQuestionSerializer(serpy.Serializer):
    slug = serpy.Field()
    title = serpy.Field()
    language = serpy.Field()

class GetQuestionSerializer(serpy.Serializer):
    slug = serpy.Field()
    title = serpy.Field()
    language = serpy.Field()
    answer = serpy.Field()

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQQuestion
        exclude = ()
