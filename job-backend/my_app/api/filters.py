# filters.py
import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    position = django_filters.CharFilter(lookup_expr='icontains')
    company = django_filters.CharFilter(lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='location__city', lookup_expr='icontains')
    country = django_filters.CharFilter(field_name='location__country', lookup_expr='icontains')
    job_type = django_filters.CharFilter(field_name='location__jobType', lookup_expr='icontains')
    experience = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Job
        fields = ['position', 'company', 'city', 'country', 'job_type', 'experience']
