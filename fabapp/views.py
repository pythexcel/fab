from rest_framework.response import Response
from rest_framework.views import APIView
from cloudinary.templatetags import cloudinary
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from fabapp.models import User, Exhibition, ExhibitFab, AvailBrand, AvailProd, AvailFurni,Message
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from exbrapp.models import Exhibitor
from exbrapp.serializers import ExhibitorSerializer
from fabrapp.models import Portfolio
from fabrapp.serializers import FabricatorSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from fabapp.serializers import (UserRegisterSerializer, UserDetailSerializer,
                                ExhibitionSerializer, ExhibitFabricators,
                                ExhibitionDetail, AvailBrandSerializer,
                                AvailFurniSerializer, AvailProdSerializer,MessageSerializer)
from exbrapp.models import Bid
from exbrapp.serializers import BidSerializer

class Test(APIView):
    def get(self, requset):
        return Response("Working")


class UserRegister(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                role = json['role']
                email = str(user)
                return Response({
                    "token": token.key,
                    "Role": role,
                    "error": False
                },status=status.HTTP_201_CREATED)
        else:
            data = {"error": True, "errors": serializer.errors}

            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UserAuth(APIView):
    def post(self, request):
        fcm = request.data.get("fcm_token")
        user = authenticate(email=request.data.get("email"),
                            password=request.data.get("password"))
        if user is not None:
            ser = UserDetailSerializer(user)
            fb = User.objects.get(id = user.id)
            fb.fcm_token = fcm
            fb.save()
            role = ser.data['role']
            print(user.id)
            try:
                token = Token.objects.get(user_id=user.id)
            except:
                token = Token.objects.create(user=user)
                print(token.key)
                print(user)
                
            return Response({"token": token.key,"role": role, "error": False})
        else:
            data = {
                "error": True,
                "msg": "User does not exist or password is wrong"
            }

            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class Userprofile(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        ser = UserDetailSerializer(request.user)
        exhibitor = Exhibitor.objects.filter(user=self.request.user)
        serializer = ExhibitorSerializer(exhibitor, many=True)
        total = serializer.data
        for elem in total:
            ua = []
            es = Bid.objects.filter(mine_exhib_id=elem['id'],work_status=True)
            if len(es) > 0:
                esr = BidSerializer(es,many=True)
                for delta in esr.data:
                    ua.append(delta["fabs_user"])
            else:
                bs = Bid.objects.filter(mine_exhib_id=elem['id'])
                bsr = BidSerializer(bs,many=True)
                for dub in bsr.data:
                    ua.append(dub["fabs_user"])
            
            elem["FAB_USER"] = ua
            
        portfolio = Portfolio.objects.filter(user=self.request.user)
        serial = FabricatorSerializer(portfolio, many=True)
        exi_bid = Bid.objects.filter(mine_exhib__user__id=request.user.id)
        exi_bid_serial = BidSerializer(exi_bid,many=True)
        fab_bid = Bid.objects.filter(fabs_user_id=request.user.id,work_status=False)
        fab_bid_serial = BidSerializer(fab_bid,many=True)

        return Response([
            ser.data, {
                "exhbhition_request": total
            }, {
                "Portfolio": serial.data
            },{
                "Exhibitor_bid_request": exi_bid_serial.data
            }, {
                "Fabricator_bid_request": fab_bid_serial.data
            }
        ])

    def put(self, request, pk=None):
        user = User.objects.get(id=pk)
        serializer = UserRegisterSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Profile Updated")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateExhibition(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = ExhibitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            detail = Exhibition.objects.get(id=serializer.data['id'])
            ser = ExhibitionDetail(detail, many=False)
            return Response("Exhibition Created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        exhibition = Exhibition.objects.all()
        serializer = ExhibitionDetail(exhibition, many=True)
        fabricator = ExhibitFab.objects.all()
        serial = ExhibitFabricators(fabricator, many=True)
        exhibhitor = Exhibitor.objects.all()
        ser = ExhibitorSerializer(exhibhitor, many=True)
        exhibitions = []
        for data in serializer.data:
            fab_list = []
            exb_list = []
            for elem in serial.data:
                if data['id'] == elem['exhibition']:
                    fab_list.append(elem)
            for detail in ser.data:
                if data['id'] == detail['exhibition']:
                    exb_list.append(detail)
            data['fabricators'] = fab_list
            data['exhibhitors'] = exb_list
            exhibitions.append(data)
        if len(exhibitions) > 0:
            return Response(exhibitions)
        else:
            return Response([])

    def put(self, request, format=None, pk=None):
        exhibition = Exhibition.objects.get(pk=pk)
        serialzier = ExhibitionSerializer(exhibition,data=request.data,partial=True)
        if serialzier.is_valid():
            serialzier.save()
            return Response("Exhibition updated")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None, pk=None):
        exhibition = Exhibition.objects.get(pk=pk)
        exhibition.delete()
        return Response({"Message":"Exhibition deleted"})


class ListExhibhition(APIView):
    def get(self, request, format=None):
        exhibition = Exhibition.objects.all()
        if exhibition is not None:
            serializer = ExhibitionDetail(exhibition, many=True)
            return Response(serializer.data)
        else:
            return Response("Exhibhition List Empty")


# List of all Fabriccatores accesible by admin
class FabricatorList(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request, format=None):

        user = User.objects.filter(role='fabricator')

        if len(user) > 0:
            serialzier = UserDetailSerializer(user, many=True)
            return Response(serialzier.data)
        else:
            return Response("Fabricator List Empty")


# List of all Exhibitors accesible by admin


class ExhibitorList(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request, format=None):

        user = User.objects.filter(role='exhibitor',
                                   is_active=True)  #filter(role="exhibitor")
        if len(user) > 0:
            serialzier = UserDetailSerializer(user, many=True)
            return Response(serialzier.data)
        else:
            return Response("Exhibitor List Empty")


# Ban a particular User from access only for admin


class BanUser(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request, format=None, pk=None):
        user = User.objects.get(id=pk)
        if user is not None:
            user.is_active = False
            user.save()
            return Response(user.email + " is banned")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExhibitionFab(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None, pk=None, pk_user=None):
        exhibhition = Exhibition.objects.get(pk=pk, Running_status=True)
        user = User.objects.get(pk=pk_user, is_active=True)
        exi = ExhibitFab(exhibition_id=exhibhition.id, user_id=user.id)
        exi.save()
        serializer = ExhibitFabricators(exi, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Addbrand(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        branding = request.data.get("brandings")
        for elem in branding:
            br = AvailBrand(user_id=self.request.user.id,
                            branding=elem['branding'])
            br.save()
        return Response("Brands added", status=status.HTTP_201_CREATED)


class Addprod(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        products = request.data.get("products")
        for elem in products:
            pr = AvailProd(user_id=self.request.user.id,
                           product=elem['product'])
            pr.save()
        return Response("Products added", status=status.HTTP_201_CREATED)


class Addfurni(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        furniture = request.data.get("furnitures")
        for elem in furniture:
            fr = AvailFurni(user_id=self.request.user.id,
                            furniture=elem['furniture'])
            fr.save()
        return Response("Furniture added", status=status.HTTP_201_CREATED)


class listItem(APIView):
    def get(self, request, format=None, pk=None):
        branding = AvailBrand.objects.all()
        serialzier = AvailBrandSerializer(branding, many=True)
        products = AvailProd.objects.all()
        serial = AvailProdSerializer(products, many=True)
        furniture = AvailFurni.objects.all()
        ser = AvailFurniSerializer(furniture, many=True)
        dict = {}
        dict['brandings'] = serialzier.data
        dict['products'] = serial.data
        dict['furnitures'] = ser.data
        return Response(dict)



class ChatMessages(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk=None):
        sender = self.request.user
        message = request.data.get("message")
        reciever = User.objects.get(id=pk)
        send_msg = Message(sender_id=sender.id,
                           receiver_id=reciever.id,
                           message=message)
        send_msg.save()
        serialzier = MessageSerializer(send_msg, many=False)
        devices = reciever.fcm_token
        devices.send_message(title="Message", body=message)
        return Response(serialzier.data, status=status.HTTP_201_CREATED)

    def get(self, request, pk=None):
        sender = self.request.user
        reciever = User.objects.get(id=pk)
        messages = Message.objects.filter(sender_id=reciever.id,
                                          receiver_id=sender.id)
        for message in messages:
            message.is_read = True
            message.save()
        serializer = MessageSerializer(messages, many=True)
        my_msg = Message.objects.filter(sender_id=sender.id,
                                        receiver_id=reciever.id)
        serial = MessageSerializer(my_msg, many=True)
        total = serializer.data + serial.data
        return JsonResponse(total, safe=False)


class ParticularUser(APIView):
    
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk=None):
        user = User.objects.get(id=pk)
        serialzizer = UserDetailSerializer(user, many=False)
        senderUser = serialzizer.data
        sender = self.request.user
        my = Message.objects.filter(sender_id=user.id,
                                    receiver_id=sender.fcm_token,
                                    is_read=False)
        serial = MessageSerializer(my, many=True)
        senderUser["messages"] = serial.data
        return Response(senderUser)

