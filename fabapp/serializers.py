from fabapp.models import (User, Exhibition, ExhibitFab,AvailBrand,AvailFurni,AvailProd)
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator


class UserRegisterSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(use_url=True, required=False)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'role', 'name', 'status', 'bio',
                  'phone', 'profile_image', 'is_active', 'is_staff',
                  'is_superuser')

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        email = validated_data.pop("email", None)
        user = User.objects.create(email=email,
                                   password=make_password(password),
                                   **validated_data)
        return user
        # is called if we save serializer if it have an instance

    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        instance.save()
        return instance


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'role', 'name', 'status', 'bio',
                  'phone', 'profile_image', 'is_active', 'is_staff',
                  'is_superuser')


class ExhibitionSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(many=False, read_only=True)

    class Meta:
        model = Exhibition
        fields = '__all__'

    def create(self, validated_data):
        user = Exhibition.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.exhibition_name = validated_data.get('exhibition_name',
                                                      instance.exhibition_name)

        instance.Description = validated_data.get('Description',
                                                  instance.Description)

        instance.Start_date = validated_data.get('Start_date',
                                                 instance.Start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.Running_status = validated_data.get('Running_status',
                                                     instance.Running_status)
        instance.save()
        return instance


class ExhibitionDetail(serializers.ModelSerializer):
    class Meta:
        model = Exhibition
        fields = '__all__'


class ExhibitFabricators(serializers.ModelSerializer):
    class Meta:
        model = ExhibitFab
        fields = '__all__'


class AvailProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailProd
        fields = '__all__'


class AvailBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailBrand
        fields = '__all__'


class AvailFurniSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailFurni
        fields = '__all__'
