from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from base_page_app.models import Company, Todo, Notes
from .serializers import CompanySerializer, TodoSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnlyUser, IsOwnerOrReadOnlyObject
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
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyObject]

    def get_queryset(self):
        return self.queryset.filter((Q(user=self.request.user) | Q(company__in=self.request.user.company_set.all())))

    def _validate_company(self, serializer):
        try:
            user_companies = Company.objects.filter(creator=self.request.user)
            company = serializer.validated_data.get('company', None)
            user = serializer.validated_data.get('user',None)
            if company:
                if not company in user_companies:
                    raise exceptions.PermissionDenied()

            if not company and user:
                if user != self.request.user:
                    raise exceptions.PermissionDenied()
        except ObjectDoesNotExist :
            raise exceptions.PermissionDenied()

        return serializer

    def perform_create(self, serializer):
        serializer = self._validate_company(serializer)
        serializer.save(user=self.request.user)

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
