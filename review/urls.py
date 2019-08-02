from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path as url
from review import views

urlpatterns = [
    url('reviews', views.UserReviewDeails.as_view()),
    url('review/<uuid:pk>', views.UserReviewDeails.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
