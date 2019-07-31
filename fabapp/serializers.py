from fabapp.models import (User, Exhibition, ExhibitFab, AvailBrand,
                           AvailFurni, AvailProd)
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
import cloudinary.uploader
import cloudinary.api


class UserRegisterSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(use_url=True, required=False)
    password = serializers.CharField(write_only=True, required=True)
    class Meta:

        model = User
        fields = ('email', 'password', 'role', 'name', 'status', 'bio',
                    'phone', 'profile_image', 'is_active', 'is_staff',
                    'is_superuser','website_link''avg_rating')

    def create(self, validated_data):
        if 'profile_image' in validated_data:
            password = validated_data.pop("password", None)
            pr_image = validated_data.pop("profile_image",None)
            im = cloudinary.uploader.upload(pr_image)
            email = validated_data.pop("email", None)
            user = User.objects.create(email=email,profile_image=im['url'],
                                    password=make_password(password),
                                    **validated_data)
        else:
            email = validated_data.pop("email", None)
            password = validated_data.pop("password", None)
            user = User.objects.create(email=email,password=make_password(password),**validated_data)

        return user
        # is called if we save serializer if it have an instance

    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        if 'profile_image'in validated_data:
            im = cloudinary.uploader.upload(instance.profile_image)    
            instance.profile_image = im['url']
        else:
            pass
        instance.save()
        return instance


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'role', 'name', 'status', 'bio',
                            'phone', 'profile_image', 'is_active','website_link','avg_rating')

class ExhibitionSerializer(serializers.ModelSerializer):
    exhibition_image = Base64ImageField(use_url=True, required=False)
    user = UserDetailSerializer(many=False, read_only=True)

    class Meta:
        model = Exhibition
        fields = '__all__'

    def create(self, validated_data):
        if 'exhibition_image' in validated_data:
            print(validated_data['exhibition_image'])
            pr_image = validated_data.pop('exhibition_image')
            print(pr_image)
            im = cloudinary.uploader.upload(pr_image)
            print(im)

            user = Exhibition.objects.create(**validated_data,
                                             exhibition_image=im['url'])
        else:
            user = Exhibition.objects.create(**validated_data)

        return user

    def update(self, instance, validated_data):
        if 'exhibition_image' in validated_data:
            instance.exhibition_image = validated_data.get(
            'exhibition_image', instance.exhibition_image)    
            im = cloudinary.uploader.upload(instance.exhibition_image)    
            instance.exhibition_image = im['url']
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
        else:

            instance.exhibition_name = validated_data.get('exhibition_name',
                                                        instance.exhibition_name)

            instance.Desciption = validated_data.get('Desciption',
                                                    instance.Desciption)

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
