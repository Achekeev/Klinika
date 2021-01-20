from rest_framework import serializers
from .models import Works


class WorksCreateSerializer(serializers.ModelSerializer):
    """ Общий список турниров """
    class Meta:
        model = Works
        fields = ('opera', 'beforeopera', 'afteropera', 'name')