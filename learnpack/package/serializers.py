import serpy
from .models import Package, Technology, Language, Skill
from rest_framework import serializers
from learnpack.email import send_email_message
from learnpack.utils import ValidationException

class GetTechnologySerializer(serpy.Serializer):
    title = serpy.Field()
    slug = serpy.Field()
    total_packages = serpy.Field()

class GetSkillSerializer(serpy.Serializer):
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
    technology = serpy.MethodField()
    skills = serpy.MethodField()
    language = serpy.MethodField()
    author = GetAuthorSerializer()
    # technology = serpy.MethodField()
    # language = serpy.MethodField()

    # def get_technology(self, obj):
    #     print(obj.technology_slug)
    #     technology = Technology.objects.filter(slug=obj.technology_slug).first()
    #     return GetTechnology(technology).data

    def get_skills(self, obj):
        all_skills = obj.skills.all()
        return [s.slug for s in all_skills]

    def get_language(self, obj):
        if obj.language is not None:
            return obj.language.slug
        else:
            return None

    def get_technology(self, obj):
        if obj.technology is not None:
            return obj.technology.slug
        else:
            return None

class PostPackageSerializer(serializers.ModelSerializer):
    skills = serializers.ListField(write_only=True)

    class Meta:
        model = Package
        exclude = ("author",)
    def validate(self, data):
        if self.context['request'].method == 'POST':
            if Package.objects.filter(slug= data["slug"]).first() is not None:
                raise serializers.ValidationError("That slug is already in use.")
        if not self.context['request'].user.is_active:
            raise serializers.ValidationError("You need to validate your email to post/update a package", code=401)

        skills = Skill.objects.all()
        if "skills" not in data or len(data["skills"]) == 0:
            raise ValidationException(f"Please specify one or up to three skills that the package teaches, options are: {','.join([s.slug for s in skills])}")
        elif len(data["skills"]) > 3:
            raise ValidationException("You can specify a max of 3 skills per package")

        langs = Language.objects.all()
        if "language" not in data:
            raise ValidationException(f"Please specify the main language for the package, options are: {','.join([l.slug for l in langs])}")
        # else:
        #     lang = Language.objects.filter(slug=data["language"]).first()
        #     if lang is None:
        #         raise ValidationException(f"Language {data['language']} its not a valid language you can apply to the package")


        for s in data["skills"]:
            skill = Skill.objects.filter(slug=s).first()
            if skill is None:
                raise ValidationException(f"Skill {s} its not part of the valid skills you can apply to the package, options are: {','.join([s.slug for s in skills])}")

        return data

    def create(self, validated_data):
        validated_data["author"]=self.context['request'].user

        package = super(PostPackageSerializer, self).create(validated_data)
        slug = package.slug
        send_email_message("package_success", self.context['request'].user.email, data= {"link": f"/v1/package/{slug}", "subject":"Package Successfully Uploaded"})
        return package

    def update(self, package ,validated_data):
        _package = package
        package = super(PostPackageSerializer, self).update(_package, validated_data)
        package.save()
        return package