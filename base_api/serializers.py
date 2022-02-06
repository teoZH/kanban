from base_page_app.models import Company, Todo, Notes
from rest_framework import serializers


class CompanySerializer(serializers.ModelSerializer):
    creator_username = serializers.SlugRelatedField(slug_field='username', source='creator', read_only=True)
    all_employees = serializers.SlugRelatedField(slug_field='username',source='employee', read_only=True,many=True)

    class Meta:
        model = Company
        fields = ('title', 'creator_username','all_employees','employee')
        extra_kwargs = {'employee': {'write_only': True}}


class TodoSerializer(serializers.ModelSerializer):
    company_name = serializers.SlugRelatedField(slug_field='title',source='company', read_only=True)
    username = serializers.SlugRelatedField(slug_field='username',source='user', read_only=True)

    class Meta:
        model = Todo
        fields = '__all__'
        extra_kwargs = {'company': {'write_only': True},
                        'user': {'write_only':True}}



class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
