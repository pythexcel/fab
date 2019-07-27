from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from fabapp.models import User, Exhibition, ExhibitFab,AvailBrand
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from exbrapp.models import Exhibitor
from exbrapp.serializers import ExhibitorSerializer
from fabrapp.models import Portfolio
from fabrapp.serializers import FabricatorSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from fabapp.serializers import (UserRegisterSerializer, UserDetailSerializer,
                                ExhibitionSerializer, ExhibitFabricators,
                                ExhibitionDetail)


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
                email = str(user)
                return Response({
                    "token": token.key,
                    "error": False
                },
                                status=status.HTTP_201_CREATED)
        else:

            data = {"error": True, "errors": serializer.errors}

            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UserAuth(APIView):
    def post(self, request):
        user = authenticate(email=request.data.get("email"),
                            password=request.data.get("password"))
        print(user)
        if user is not None:
            try:
                token = Token.objects.get(user_id=user.id)
            except:
                token = Token.objects.create(user=user)
                print(token.key)
                print(user)
            return Response({"token": token.key, "error": False})
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
        portfolio = Portfolio.objects.filter(user=self.request.user)
        serial = FabricatorSerializer(portfolio, many=True)
        return Response([
            ser.data, {
                "exhbhition_request": serializer.data
            }, {
                "Portfolio": serial.data
            }
        ])

    def put(self, request, pk=None):

        user = User.objects.get(id=pk)
        serializer = UserRegisterSerializer(user,
                                            data=request.data,
                                            partial=True)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateExhibition(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = ExhibitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            return Response([], status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None, pk=None):
        exhibition = Exhibition.objects.get(pk=pk)
        serialzier = ExhibitionSerializer(exhibition,
                                          data=request.data,
                                          partial=True)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serialzier.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None, pk=None):
        exhibition = Exhibition.objects.get(pk=pk)
        exhibition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListExhibhition(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        exhibition = Exhibition.objects.filter(Running_status=True)
        if exhibition is not None:
            serializer = ExhibitionDetail(exhibition, many=True)
            return Response(serializer.data)
        else:
            return Response([], status=status.HTTP_400_BAD_REQUEST)


# List of all Fabriccatores accesible by admin
class FabricatorList(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request, format=None):

        user = User.objects.filter(role='fabricator', is_active=True)

        if len(user) > 0:
            serialzier = UserDetailSerializer(user, many=True)
            return Response(serialzier.data)
        else:
            return Response([], status=status.HTTP_400_BAD_REQUEST)


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
            return Response([], status=status.HTTP_400_BAD_REQUEST)


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


# class Additems(APIView):
#     def post(self, request,format=None):
#         brandiings = request.data.get("brandings")
#         for data in brandiings:
#             br = AvailBrand.objects.create(branding=data,user_id=self.request.user.id)
#             serializer = AvailBrandSerializer(br,many=True)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         # print(brandiings)
#         # serializer = AvailBrandSerializer(brandiings,many=True)
#         # print(serializer.data)
#         # if serializer.is_valid():
#         #     serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
