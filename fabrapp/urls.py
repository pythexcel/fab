from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path as url
from fabrapp import views

urlpatterns = [
    url('portfolio', views.FabricatorPortfolio.as_view()),
    url('portfolio/<uuid:pk>', views.FabricatorPortfolio.as_view()),
    url('bidresponse/<uuid:pk>', views.BidResponse.as_view()),
    url('bidresponse', views.BidResponse.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
