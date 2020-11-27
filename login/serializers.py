from rest_framework import serializers
from .models import Login

#Lead serializer
class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'