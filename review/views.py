from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from review.models import Review
from fabapp.models import User
from fabapp.serializers import UserDetailSerializer
from review.serializers import ReviewSeializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser



class UserReviewDeails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,format=None):
        lg_user = self.request.user
        user = Review.objects.filter(user_id=lg_user.id)
        ser = ReviewSeializer(user,many=True)
        mine = Review.objects.filter(rated_user_id=lg_user.id)
        serial = ReviewSeializer(mine,many=True)
        total = ser.data + serial.data
        return Response(total)
        
    def post(self,request,pk=None):
        comment = request.data.get("comment")
        rating = request.data.get("rating")
        user_one = self.request.user
        user_two = User.objects.get(id=pk)
        reviewed = Review.objects.filter(user_id=user_one.id,rated_user_id=user_two.id)
        if len(reviewed) == 0:
            review = Review(user_id=user_one.id,rated_user_id=user_two.id,comment=comment,rating=rating)
            review.save()
            serializer = ReviewSeializer(review,many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("you already reviewed this User", status=status.HTTP_201_CREATED)


        
        

        















