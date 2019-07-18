from rest_framework import serializers
from fabrapp.models import (Portfolio)
from fabapp.serializers import UserDetailSerializer


class FabricatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('id', 'image')
