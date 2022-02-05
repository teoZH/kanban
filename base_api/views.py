from rest_framework.viewsets import ModelViewSet
from base_page_app.models import Company, Todo, Notes
from .serializers import CompanySerializer
from rest_framework.permissions import IsAuthenticated



class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
