from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from fabrapp.models import Portfolio
from fabapp.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from fabrapp.serializers import FabricatorSerializer
from fabrapp.permissions import IsFabricator
from fabapp.serializers import UserDetailSerializer
from exbrapp.models import Bid
from exbrapp.serializers import BidSerializer
import cloudinary.uploader

def modify_input_for_multiple_files(image):
    dict = {}
    dict['image'] = image
    return dict


class FabricatorPortfolio(APIView):
    # parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    permission_classes = (IsAuthenticated, IsFabricator)

    def get(self, request):
        all_images = Portfolio.objects.filter(user=self.request.user)
        serializer = FabricatorSerializer(all_images, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        images = request.data['images']
        flag = 1
        for img_name in images:
            up_image = "data:image/gif;base64,"+img_name['image']
            im = cloudinary.uploader.upload(up_image)
            md = Portfolio(user_id=self.request.user.id,image=im['url'])
            md.save()
        return Response("Portfolio Added", status=status.HTTP_201_CREATED)
            
    def delete(self, request, pk, format=None):
        exi = Portfolio.objects.get(user=self.request.user, pk=pk)
        exi.delete()
        return Response("Portfolio Image Deleted",status=status.HTTP_204_NO_CONTENT)

class BidResponse(APIView):
    def get(self,request,format=None):
        user = self.request.user
        print(user.id)

        bids = Bid.objects.filter(fabs_user_id=user.id,work_status=False)
        serializer = BidSerializer(bids,many=True)
        return Response(serializer.data)

    def put(self,request,format=None,pk=None):
        comment = request.data.get("comment")
        total_price = request.data.get("total_price")
        bid = Bid.objects.get(id=pk)
        bid.comment = comment
        bid.total_price = total_price
        bid.response_status = True
        bid.save()
        serial = BidSerializer(bid,many=False)
        return Response(serial.data)



class BidTaskCompleted(APIView):
    def put(self,request,format=None,pk=None):
        bid = Bid.objects.get(id=pk)
        print(bid)
        if bid.work_status is True:
            bid.complete_status = True
            bid.save()
            serial = BidSerializer(bid,many=False)
            return Response(serial.data)
        else:
            return Response("This Bid work is not yet started",status=status.HTTP_400_BAD_REQUEST)