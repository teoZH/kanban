from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from base_page_app.models import Company, Todo, Notes
from .serializers import CompanySerializer, TodoSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnlyUser, IsOwnerOrReadOnlyObject, IsOwnerOrReadOnlyTodo
from rest_framework import exceptions
from django.core.exceptions import ObjectDoesNotExist


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyUser]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)


class TodoViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyTodo]

    def get_queryset(self):
        return self.queryset.filter((Q(user=self.request.user) | Q(company__in=self.request.user.company_set.all())))

    def _validate_user(self, serializer):
        user_companies = self.request.user.company_set.all()
        company = serializer.validated_data.get('company', None)
        user = serializer.validated_data.get('user', None)
        if not user:
            serializer.validated_data['user'] = self.request.user
        if user and company:
            if not user in company.employee.all() and user != company.creator:
                raise exceptions.PermissionDenied()
        if not company is None and not company in user_companies and self.request.method == 'POST':
            raise exceptions.PermissionDenied()
        if not company and user:
            if self.request.user != user:
                raise exceptions.PermissionDenied()
        return serializer

    def _validate_company(self, serializer):
        todo = self.get_object()
        serializer = self._validate_user(serializer)
        company = serializer.validated_data.get('company', None)
        if company and todo.company:
            if company.creator != todo.company.creator and self.request.user != todo.company.creator:
                raise exceptions.PermissionDenied()
            if self.request.user != todo.company.creator and serializer.validated_data['user'] != todo.user:
                raise exceptions.PermissionDenied()
        return serializer

    def perform_create(self, serializer):
        serializer = self._validate_user(serializer)
        serializer.save()

    def perform_update(self, serializer):
        serializer = self._validate_company(serializer)
        return super().perform_update(serializer)


class NotesViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyObject]
    serializer_class = NoteSerializer
    queryset = Notes.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
