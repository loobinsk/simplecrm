from rest_framework import generics
from ..models import SelectedData
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import SubjectSerializer


class SubjectListView(generics.ListAPIView):
	queryset = SelectedData.objects.all()
	serializer_class = SubjectSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['user']
	
class SubjectDetailView(generics.RetrieveAPIView):
	queryset = SelectedData.objects.all()
	serializer_class = SubjectSerializer