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
    company = serializers.SlugRelatedField(read_only=True, slug_field='title')
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Todo
        fields = '__all__'


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
