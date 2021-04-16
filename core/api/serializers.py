from rest_framework import serializers
from ..models import SelectedData

class SubjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = SelectedData
		fields = ['user', 'data']