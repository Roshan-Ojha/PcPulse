from django.urls import path

from api.views import PCInfoAPI,SystemInfoAPI

urlpatterns = [
    path('pcinfo/', PCInfoAPI.as_view(), name="api info"),
    path('systeminfo/',SystemInfoAPI.as_view(), name="system_info")
]
