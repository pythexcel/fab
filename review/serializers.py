from rest_framework import serializers
from fabapp.serializers import UserDetailSerializer
from review.models import Review


class ReviewSeializer(serializers.ModelSerializer):
    user = UserDetailSerializer(many=False)
    rated_user = UserDetailSerializer(many=False)

    class Meta:
        model = Review
        fields = '__all__'