from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path as url
from exbrapp import views

urlpatterns = [
    url('exhibitor_request/<int:pk>', views.ExhibitorRequire.as_view()),
    url('exhibitor_request', views.ExhibitorRequire.as_view()),
    url('exhibitor_detail/<int:pk>', views.ExhibhitDetails.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
