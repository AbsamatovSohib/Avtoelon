from django.shortcuts import render
from rest_framework import routers, serializers, viewsets, generics
from avto.models import Post
from avto.serializers import PostSerializer


# Create your views here.
class MainPostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all().order_by("-published_at")
    serializer_class = PostSerializer
    filterset_fields = ("subcategory__category",)
