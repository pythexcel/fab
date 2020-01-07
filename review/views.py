from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from review.models import Review
from fabapp.models import User
from exbrapp.models import Bid
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
        rating = request.data.get("rating")
        user_one = self.request.user
        user_two = User.objects.get(id=pk)
        review = Review(user_id=user_one.id,rated_user_id=user_two.id,rating=rating)
        review.save()
        return Response({"Message":"Rating submitted"})
        

        
        

        















