from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from fabapp.models import User, Exhibition
from exbrapp.models import Exhibitor
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from exbrapp.serializers import (ExhibitorSerializer)
from exbrapp.permissions import IsExhibitor


class ExhibitorRequire(APIView):
    permission_classes = (IsAuthenticated,IsExhibitor )

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
    permission_classes = (IsAuthenticated,IsExhibitor )

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
