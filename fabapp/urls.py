from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path as url
from fabapp import views

urlpatterns = [
    url('test', views.Test.as_view()),
    url('register', views.UserRegister.as_view()),
    url('login', views.UserAuth.as_view()),
    url('profile', views.Userprofile.as_view()),
    url('listexhbiton',views.ListExhibhition.as_view()),
    url('exhibition_create', views.CreateExhibition.as_view()),
    url('exhibition_update/<int:pk>', views.CreateExhibition.as_view()),
    url('exifab/<int:pk>/<int:pk_user>', views.ExhibitionFab.as_view()),
    url('exhibtorlist', views.ExhibitorList.as_view()),
    url('fabricatorlist', views.FabricatorList.as_view()),
    url('banuser/<int:pk>', views.BanUser.as_view()),
    url('profile/<int:pk>', views.Userprofile.as_view())
    # url('addprod', views.Additems.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
