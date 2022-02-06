from rest_framework.viewsets import ModelViewSet
from base_page_app.models import Company, Todo, Notes
from .serializers import CompanySerializer, TodoSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnlyUser, IsOwnerOrReadOnlyTodo


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

    def _validate_company(self, serializer):
        try:
            user_companies = Company.objects.filter(creator=self.request.user)
            company = serializer.validated_data.get('company', None)
            if company:
                if not company in user_companies:
                    serializer.validated_data['company'] = None
        except Company.DoesNotExist:
            raise ValueError('Do not Exist')

        return serializer

    def perform_create(self, serializer):
        serializer = self._validate_company(serializer)
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer = self._validate_company(serializer)
        return super().perform_update(serializer)
