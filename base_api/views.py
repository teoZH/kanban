from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from base_page_app.models import Company, Todo, Notes
from .serializers import CompanySerializer, TodoSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnlyUser, IsOwnerOrReadOnlyObject, IsOwnerOrReadOnlyTodo
from rest_framework import exceptions
from .filters import CompanyTodoNotesFilter


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyUser]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(Q(creator=self.request.user) | Q(employee=self.request.user))


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
                raise exceptions.NotFound()
        if not company is None and not company in user_companies and self.request.method == 'POST':
            raise exceptions.NotFound()
        if not company and user:
            if self.request.user != user:
                raise exceptions.NotFound()
        return serializer

    def _validate_company(self, serializer):
        todo = self.get_object()
        serializer = self._validate_user(serializer)
        company = serializer.validated_data.get('company', None)
        if company and todo.company:
            if company.creator != todo.company.creator and self.request.user != todo.company.creator:
                raise exceptions.NotFound()
            if self.request.user != todo.company.creator and serializer.validated_data['user'] != todo.user:
                raise exceptions.NotFound()
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
    filterset_class = CompanyTodoNotesFilter

    def get_queryset(self):
        return self.queryset.filter((Q(user=self.request.user) | Q(todo__company__in=self.request.user.employee.all())))

    def __validate_todo(self, serializer):
        todo = serializer.validated_data.get('todo', None)
        if not todo:
            raise exceptions.NotFound()

        if todo.company:
            if not (todo.company.creator == self.request.user or todo.user == self.request.user):
                raise exceptions.NotFound()
        else:
            if self.request.user != todo.user:
                raise exceptions.NotFound()
        return serializer

    def perform_create(self, serializer):
        serializer = self.__validate_todo(serializer)
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer = self.__validate_todo(serializer)
        serializer.save(user=self.request.user)

# TODO should add filters too that would allow user too see notes of todos that are joint
# ex. boss and worker can see notes of A jointtodo
# TODO add some filters???? should decide what kind of ??
