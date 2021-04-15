from rest_framework import generics
from ..models import SelectedData
from .serializers import SubjectSerializer


class SubjectListView(generics.ListAPIView):
	queryset = SelectedData.objects.all()
	serializer_class = SubjectSerializer
	
class SubjectDetailView(generics.RetrieveAPIView):
	queryset = SelectedData.objects.all()
	serializer_class = SubjectSerializer