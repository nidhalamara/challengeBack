from rest_framework import serializers
from .models import Proposition

class PropositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposition
        fields = '__all__'
        read_only_fields = ['user']  # Ensure the user field is read-only
