from rest_framework.response import Response
from rest_framework.views import APIView
from fabapp.models import User, Exhibition, ExhibitFab
from fabapp.serializers import ExhibitionSerializer
from exbrapp.models import Exhibitor,Bid
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from exbrapp.serializers import (ExhibitorSerializer,BidSerializer)
from exbrapp.permissions import IsExhibitor
from fabapp.serializers import UserDetailSerializer, ExhibitFabricators
from fcm_django.models import FCMDevice


class ExhibitorRequire(APIView):
    permission_classes = (IsAuthenticated, IsExhibitor)

    def post(self, request, format=None, pk=None):
        exhibhition = Exhibition.objects.get(pk=pk)
        serializer = ExhibitorSerializer(data=request.data,many=False)
        print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save(user=self.request.user,
                            exhibition_id=exhibhition.id)
            return Response("Request created for exhbhition", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        serializer = Exhibitor.objects.filter(user=request.user)
        if serializer is not None:
            exhibhit = ExhibitorSerializer(serializer, many=True)
            return Response(exhibhit.data)
        else:
            return Response([])


class ExhibhitDetails(APIView):
    permission_classes = (IsAuthenticated, IsExhibitor)

    def get_object(self, pk):
        try:
            return Exhibitor.objects.get(pk=pk, user=self.request.user)
        except Exhibitor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        exi = self.get_object(pk)
        serailizer = ExhibitorSerializer(exi)
        return Response(serailizer.data)

    def put(self, request, pk, format=None):
        exi = self.get_object(pk)
        serializer = ExhibitorSerializer(exi, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        exi = self.get_object(pk)
        exi.delete()
        return Response("Exhibtion Request Deleted",status=status.HTTP_204_NO_CONTENT)


class Fabricatorslist(APIView):
    
    def get(self, request, format=None, pk=None):
        exi = ExhibitFab.objects.filter(exhibition_id=pk)
        serializer = ExhibitFabricators(exi, many=True)
        user_list = []
        for data in serializer.data:
            user = User.objects.get(id=data['user'],is_active=True)
            serial = UserDetailSerializer(user, many=False)
            tp = serial.data
            tp['selected'] = False
            user_list.append(tp)

        return Response(user_list)


class Fabricator_dt(APIView):
    
    def get(self, request, format=None, pk=None, user_pk=None):
        exi = ExhibitFab.objects.get(exhibition_id=pk, user_id=user_pk)
        serializer = ExhibitFabricators(exi, many=False)
        print(serializer.data)
        user = User.objects.get(id=serializer.data['user'],is_active=True)
        serial = UserDetailSerializer(user, many=False)
        return Response(serial.data)

class CreateBid(APIView):
    permission_classes = (IsAuthenticated, IsExhibitor)

    def get(self,request,format=None):
        user = self.request.user 
        bid = Bid.objects.filter(mine_exhib__user__id=user.id)
        serializer = BidSerializer(bid, many=True)
        return Response(serializer.data)


    def post(self,request,format=None,exi_pk=None):
        user = self.request.user
        own_ser = UserDetailSerializer(user,many=False)
        my_name = own_ser.data['company_name']
        existed = []
        confirm = []
        for data in request.data['fab_ids']:
            fab_user = User.objects.get(pk=data,is_active=True)
            exhibhition = Exhibitor.objects.get(pk=exi_pk)
            exi_ser = ExhibitorSerializer(exhibhition,many=False)
            exhibition_name = exi_ser.data['exhibition']['exhibition_name']
            ser = UserDetailSerializer(fab_user,many=False)
            devices = FCMDevice.objects.get(user=ser.data['id'])
            devices.send_message(title="Notification",body="Notification from "+ my_name+ " You have beed Invited for "+ exhibition_name)
            bid = Bid.objects.filter(fabs_user_id=fab_user.id,mine_exhib_id=exhibhition.id)
            if not bid:
                confirm.append(fab_user.company_name)
                bid = Bid(fabs_user_id=fab_user.id,mine_exhib_id=exhibhition.id)
                bid.save()
                serializer = BidSerializer(bid, many=False)
                devices = FCMDevice.objects.get(user=ser.data['id'])
                devices.send_message(title="Notification",body="Notification from "+ my_name+ " You have beed Invited for "+ exhibition_name)
            else:
                existed.append(fab_user.company_name)
        if confirm:
            if existed:
                return Response({"success":True,"Message": "already sended to {}".format(",".join(existed))})
        if confirm:
            return Response({"success":True})
        if existed:
            return Response({"Message": "already sended to {}".format(",".join(existed))})


    def put(self,request,format=None,pk=None):
        bid = Bid.objects.get(id=pk)
        bid.work_status = True
        bid.save()
        ser = BidSerializer(bid,many=False)
        return Response(ser.data)
