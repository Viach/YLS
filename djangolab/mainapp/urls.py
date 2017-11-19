from django.conf.urls import url
from mainapp.views import LabDetailView

urlpatterns = [
    url(r'^(?P<pk>\d*)$', LabDetailView.as_view(), name='home'),
]
