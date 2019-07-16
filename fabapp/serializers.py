from fabapp.models import Exhibitor, FurnitureExhibitorDetail, BrandingExhibitorDetail, ProductExhibitorDetail, User, Exhibition
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator


class UserRegisterSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(use_url=True)
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
        password = validated_data.pop("password")
        instance.__dict__.update(validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'role', 'name', 'status', 'bio',
                  'phone', 'profile_image', 'is_active', 'is_staff',
                  'is_superuser')


class ExhibitionSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(many=False, read_only=True)

    class Meta:
        model = Exhibition
        fields = ('id', 'user', 'exhibition_name')

    def create(self, validated_data):
        user = Exhibition.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.exhibition_name = validated_data.get('exhibition_name',
                                                      instance.exhibition_name)
        instance.save()
        return instance


class FurnituredDetail(serializers.ModelSerializer):
    class Meta:
        model = FurnitureExhibitorDetail
        fields = ('id', 'furniture')


class BrandingDetail(serializers.ModelSerializer):
    class Meta:
        model = BrandingExhibitorDetail
        fields = ('id', 'branding')


class ProductDetail(serializers.ModelSerializer):
    class Meta:
        model = ProductExhibitorDetail
        fields = ('id', 'product')


class ExhibitionDetail(serializers.ModelSerializer):
    class Meta:
        model = Exhibition
        fields = ('id', 'exhibition_name')


class ExhibitorSerializer(serializers.ModelSerializer):
    furnitures = FurnituredDetail(many=True)
    brandings = BrandingDetail(many=True)
    products = ProductDetail(many=True)
    user = UserDetailSerializer(many=False, read_only=True)
    exhibition = ExhibitionDetail(many=False, read_only=True)

    class Meta:
        model = Exhibitor
        fields = ('id', 'exhibition', 'size', 'stall_no', 'color_theme',
                  'carpet', 'extra', 'created_on', 'furnitures', 'brandings',
                  'products', 'user')

    def create(self, validated_data):
        furniture_data = validated_data.pop('furnitures')
        branding_data = validated_data.pop('brandings')
        product_data = validated_data.pop('products')
        exi = Exhibitor.objects.create(**validated_data)
        for data in furniture_data:
            FurnitureExhibitorDetail.objects.create(furnitures=exi, **data)
        for elem in branding_data:
            BrandingExhibitorDetail.objects.create(brandings=exi, **elem)
        for detail in product_data:
            ProductExhibitorDetail.objects.create(products=exi, **detail)
        return exi

    def update(self, instance, validated_data):
        furniture_data = validated_data.pop('furnitures')
        branding_data = validated_data.pop('brandings')
        product_data = validated_data.pop('products')
        instance.size = validated_data.get('size', instance.size)
        instance.stall_no = validated_data.get('stall_no', instance.stall_no)
        instance.color_theme = validated_data.get('color_theme',
                                                  instance.color_theme)
        instance.carpet = validated_data.get('carpet', instance.carpet)
        instance.extra = validated_data.get('extra', instance.extra)
        instance.save()
        return instance


# class FabricatorSerializer(serializers.ModelSerializer):
#     user = UserSerialzier(many=False, read_only=True)
#     portfolio = PortfolioDetail(many=True)

#     class Meta:
#         model = FabricatorDetail
#         fields = ('id', 'user', 'portfolio')

#     def create(self, validated_data):
#         protfolio_detai = validated_data.pop('portfolio')
#         exi = PortfolioFabricator.objects.create(**validated_data)
#         for data in PortfolioDetail:
#             FurnitureExhibitorDetail.objects.create(furnitures=exi, **data)
#         return exi
