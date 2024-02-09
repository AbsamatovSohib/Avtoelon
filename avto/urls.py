from django.urls import path, include
from avto import views

urlpatterns = [path("main/", views.MainPostListAPIView.as_view())]
