from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path as url
from fabapp import views

urlpatterns = [
    url('test', views.Test.as_view()),
    url('register', views.UserRegister.as_view()),
    url('login', views.UserAuth.as_view()),
    url('profile', views.Userprofile.as_view()),
    url('profile/<uuid:pk>', views.Userprofile.as_view()),
    url('listexhbiton',views.ListExhibhition.as_view()),
    url('exhibition_create', views.CreateExhibition.as_view()),
    url('exhibition_update/<uuid:pk>', views.CreateExhibition.as_view()),
    url('exifab/<uuid:pk>/<uuid:pk_user>', views.ExhibitionFab.as_view()),
    url('exhibtorlist', views.ExhibitorList.as_view()),
    url('fabricatorlist', views.FabricatorList.as_view()),
    url('banuser/<uuid:pk>', views.BanUser.as_view()),
    url('profile/<uuid:pk>', views.Userprofile.as_view()),
    url('addprod', views.Addprod.as_view()),
    url('addbrand', views.Addbrand.as_view()),
    url('addfunr', views.Addfurni.as_view()),
    url('listitem', views.listItem.as_view()),
    url('chat/<uuid:pk>/<uuid:pk_exi>', views.ChatMessages.as_view()),
    url('partuser', views.ParticularUser.as_view())

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
