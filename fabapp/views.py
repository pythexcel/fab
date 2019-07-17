from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from fabapp.models import Exhibitor, User, Exhibition, Portfolio, ExhibitFab
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from fabapp.serializers import (UserRegisterSerializer, UserDetailSerializer,
                                ExhibitionSerializer, ExhibitorSerializer,
                                ExhibitionDetail, FabricatorSerializer,
                                ExhibitFabricators)


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
        return Response(ser.data)


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
        if exhibition is not None:
            serializer = ExhibitionDetail(exhibition, many=True)
            return Response(serializer.data)
        else:
            return Response([], status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None, pk=None):
        exhibition = Exhibition.objects.get(pk=pk)
        serialzier = ExhibitionSerializer(exhibition, data=request.data)
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
        exhibition = Exhibition.objects.all()
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
            serialzier = UserSerialzier(user, many=True)
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
            serialzier = UserSerialzier(user, many=True)
            return Response(serialzier.data)
        else:
            return Response([], status=status.HTTP_400_BAD_REQUEST)


# Ban a particular User from access only for admin


class BanUser(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request, format=None):
        ban_id = request.data.get("ban_id")
        user = User.objects.get(pk=ban_id)
        if user is not None:
            user.is_active = False
            user.save()
            return Response(user.username + " is banned")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExhibitorRequire(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None, pk=None):
        exhibhition = Exhibition.objects.get(pk=pk)
        serializer = ExhibitorSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save(user=self.request.user,
                            exhibition_id=exhibhition.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        serializer = Exhibitor.objects.filter(user=request.user)
        if serializer is not None:
            exhibhit = ExhibitorSerializer(serializer, many=True)
            return Response(exhibhit.data)
        else:
            return Response([], status=status.HTTP_400_BAD_REQUEST)


class ExhibhitDetails(APIView):
    permission_classes = (IsAuthenticated, )

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
        serializer = ExhibitorSerializer(exi, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        exi = self.get_object(pk)
        exi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def modify_input_for_multiple_files(image):
    dict = {}
    dict['image'] = image
    return dict


class FabricatorPortfolio(APIView):
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    permission_classes = (IsAuthenticated, )

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


class ExhibitionFab(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None, pk=None, pk_user=None):
        exhibhition = Exhibition.objects.get(pk=pk)
        user = User.objects.get(pk=pk_user)
        exi = ExhibitFab(exhibition_id=exhibhition.id, user_id=user.id)
        exi.save()
        serializer = ExhibitFabricators(exi,many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        