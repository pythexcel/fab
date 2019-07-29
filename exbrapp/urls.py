from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path as url
from exbrapp import views

urlpatterns = [
    url('exhibitor_request/<int:pk>', views.ExhibitorRequire.as_view()),
    url('exhibitor_request', views.ExhibitorRequire.as_view()),
    url('exhibitor_detail/<int:pk>', views.ExhibhitDetails.as_view()),
    url('fabricators/<int:pk>', views.Fabricatorslist.as_view()),
    url('fabricator_dt/<int:pk>/<int:user_pk>', views.Fabricator_dt.as_view()),
    url('create_bid/<int:pk>/<int:exi_pk>', views.CreateBid.as_view()),
    url('create_bid', views.CreateBid.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
