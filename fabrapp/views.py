from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from fabrapp.models import Portfolio
from fabapp.models import User
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from fabrapp.serializers import FabricatorSerializer
from fabrapp.permissions import IsFabricator


def modify_input_for_multiple_files(image):
    dict = {}
    dict['image'] = image
    return dict


class FabricatorPortfolio(APIView):
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    permission_classes = (IsAuthenticated, IsFabricator)

    def get(self, request):
        all_images = Portfolio.objects.filter(user=self.request.user)
        serializer = FabricatorSerializer(all_images, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        images = dict((request.data).lists())['image']
        print(images)
        arr = []
        flag = 1
        for img_name in images:
            modified_data = modify_input_for_multiple_files(img_name)
            file_serializer = FabricatorSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save(user=self.request.user)
                arr.append(file_serializer.data)
            else:
                flag = 0
        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        exi = Portfolio.objects.get(user=self.request.user, pk=pk)
        exi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
