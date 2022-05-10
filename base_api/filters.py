import django_filters
import django_filters as filters
from base_page_app.models import Company, Todo, Notes


class CompanyTodoNotesFilter(filters.FilterSet):
    company = filters.NumberFilter(field_name='todo__company__pk', lookup_expr='exact')

    class Meta:
        model = Notes
        fields = ['company']
