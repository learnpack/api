import serpy
from .models import Package, Technology, Language
from rest_framework import serializers
from learnpack.email import send_email_message

class GetTechnologySerializer(serpy.Serializer):
    title = serpy.Field()
    slug = serpy.Field()
    total_packages = serpy.Field()

class GetLanguageSerializer(serpy.Serializer):
    title = serpy.Field()
    slug = serpy.Field()
    total_packages = serpy.Field()

class GetAuthorSerializer(serpy.Serializer):
    username = serpy.Field()
    first_name = serpy.Field()
    last_name = serpy.Field()

class GetPackageSerializer(serpy.Serializer):
    """The serializer schema definition."""
    # Use a Field subclass like IntField if you need more validation.
    title = serpy.Field()
    slug = serpy.Field()
    description = serpy.Field()
    repository = serpy.Field()
    technology = GetTechnologySerializer(required= False)
    language = GetLanguageSerializer(required = False)
    author = GetAuthorSerializer()
    # technology = serpy.MethodField()
    # language = serpy.MethodField()

    # def get_technology(self, obj):
    #     print(obj.technology_slug)
    #     technology = Technology.objects.filter(slug=obj.technology_slug).first()
    #     return GetTechnology(technology).data

    # def get_language(self, obj):
    #     language = Language.objects.filter(slug=obj.language_slug).first()
    #     return GetLanguage(language).data

class PostPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        exclude = ("author",)
    def create(self, validated_data):
        validated_data["author"]=self.context['request'].user
        print(self.context)
        print(validated_data)
        package = super(PostPackageSerializer, self).create(validated_data)
        slug = package.slug
        send_email_message("package_success", self.context['request'].user.email, data= {"link": f"/v1/package/{slug}", "subject":"Package Successfully Uploaded"})
        return package