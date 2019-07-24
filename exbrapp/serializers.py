from exbrapp.models import (Exhibitor, ProductExhibitorDetail,
                            BrandingExhibitorDetail, FurnitureExhibitorDetail,Bid)
from rest_framework import serializers
from fabapp.serializers import UserDetailSerializer, ExhibitionDetail



class FurnituredDetail(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = FurnitureExhibitorDetail
        fields = ('id', 'furniture')


class BrandingDetail(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = BrandingExhibitorDetail
        fields = ('id', 'branding')


class ProductDetail(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ProductExhibitorDetail
        fields = ('id', 'product')


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
                  'products', 'user', 'website_link')

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
        print(validated_data)
        instance.size = validated_data.get('size', instance.size)
        instance.stall_no = validated_data.get('stall_no', instance.stall_no)
        instance.color_theme = validated_data.get('color_theme',
                                                  instance.color_theme)
        instance.carpet = validated_data.get('carpet', instance.carpet)
        instance.extra = validated_data.get('extra', instance.extra)
        instance.website_link = validated_data.get('website_link',
                                                   instance.website_link)
        instance.save()
        
        if 'furnitures' in validated_data:

            furniture_data = validated_data.get('furnitures')
            for data in furniture_data:
                data_id = data.get('id', None)
                if data_id:
                    fur_data = FurnitureExhibitorDetail.objects.get(
                       id=data_id, furnitures=instance)
                    fur_data.furniture = data.get('furniture', fur_data.furniture)
                    fur_data.save()
                else:
                    fur_data = FurnitureExhibitorDetail.objects.create(
                        **data, furnitures=instance)

        if 'brandings' in validated_data:
            branding_data = validated_data.get('brandings')
            for elem in branding_data:
                elem_id = elem.get('id', None)
                if elem_id:
                    brd_data = BrandingExhibitorDetail.objects.get(
                        id=elem_id, brandings=instance)
                    brd_data.branding = elem.get('branding', brd_data.branding)
                    brd_data.save()
                else:
                    brd_data = BrandingExhibitorDetail.objects.create(
                        **elem, brandings=instance)
        
        if 'products' in validated_data:
            product_data = validated_data.get('products')
            for detail in product_data:
                detail_id = detail.get('id', None)
                
                if detail_id:
                    
                    pro_data = ProductExhibitorDetail.objects.get(
                        id=detail_id, products=instance)
                      
                    pro_data.product = detail.get('product', pro_data.product)
                    print(pro_data.product)
                   
                    pro_data.save()
                else:
                    pro_data = ProductExhibitorDetail.objects.create(
                        **detail, products=instance)
                     
        return instance

class BidSerializer(serializers.ModelSerializer):
    mine_exhib = ExhibitorSerializer(many=False)
    fabs_user = UserDetailSerializer(many=False)
    class Meta:
        model = Bid
        fields = '__all__'