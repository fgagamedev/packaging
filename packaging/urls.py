from django.conf.urls import url, include
from . import views

from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'package', views.PackageViewSet)

urlpatterns = [
    # url(r'^', include(router.urls)),
    url('', views.PackageViewSet.as_view({'post':'post'}))
]
