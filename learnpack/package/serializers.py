import serpy
from .models import Package, Technology, Language
from rest_framework import serializers

class GetTechnology(serpy.Serializer):
    title = serpy.Field()
    slug = serpy.Field()
class GetLanguage(serpy.Serializer):
    title = serpy.Field()
    slug = serpy.Field()

class GetPackageSerializer(serpy.Serializer):
    """The serializer schema definition."""
    # Use a Field subclass like IntField if you need more validation.
    title = serpy.Field()
    slug = serpy.Field()
    description = serpy.Field()
    repository = serpy.Field()
    # technology = serpy.MethodField()
    # language = serpy.MethodField()

    # def get_technology(self, obj):
    #     technology = Technology.objects.get(slug=obj.technology_slug)
    #     return GetTechnology(technology).data

    # def get_language(self, obj):
    #     language = Language.objects.get(slug=obj.language_slug)
    #     return GetLanguage(language).data

# class GetPackageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Package
#         exclude = ()