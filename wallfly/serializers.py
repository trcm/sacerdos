from rest_framework import serializers
from wallfly.models import Property


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
