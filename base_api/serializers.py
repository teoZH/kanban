from base_page_app.models import Company, Todo, Notes
from rest_framework import serializers


class CompanySerializer(serializers.ModelSerializer):
    creator_username = serializers.SlugRelatedField(slug_field='username', source='creator', read_only=True)
    all_employees = serializers.SlugRelatedField(slug_field='username', source='employee', read_only=True, many=True)

    class Meta:
        model = Company
        fields = ('id', 'title', 'creator_username', 'all_employees', 'employee')
        extra_kwargs = {'employee': {'write_only': True}}


class TodoSerializer(serializers.ModelSerializer):
    company_name = serializers.SlugRelatedField(slug_field='title', source='company', read_only=True)
    username = serializers.SlugRelatedField(slug_field='username', source='user', read_only=True)

    class Meta:
        model = Todo
        exclude = ('date',)
        extra_kwargs = {'company': {'write_only': True},
                        'user': {'write_only': True},
                        }

    def validate(self, attrs):
        if 'in_progress' in attrs and 'is_done' in attrs:
            if attrs['in_progress'] is True and attrs['is_done'] is True:
                raise serializers.ValidationError({'error': "Both fields cannot be true"})
        return attrs


class NoteSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(slug_field='username', source='user', read_only=True)
    todo_title = serializers.SlugRelatedField(slug_field='title', source='todo', read_only=True)

    class Meta:
        model = Notes
        fields = ('id', 'todo_title', 'description', 'todo', 'username')
        extra_kwargs = {
            "todo": {'write_only': True},
        }

