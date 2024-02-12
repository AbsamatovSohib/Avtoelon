from django.shortcuts import render
from rest_framework import routers, serializers, viewsets, generics
from avto.models import Post,Region, District
from avto.serializers import PostSerializer,StatisticBuyCarSerializer
from django.db.models import Count
from rest_framework.response import Response


# Create your views here.
class MainPostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all().order_by("-published_at")
    serializer_class = PostSerializer
    filterset_fields = ("subcategory__category",)


class StatisticBuyCarView(generics.ListAPIView):

    queryset = District.objects.all()
    serializer_class =StatisticBuyCarSerializer
    
    def get(self, request):
        regions = District.objects.annotate(post_count=Count('posts'))
        data = [
            {
            'region_name': region.title,
            'post_count': region.post_count
        } for region in regions
        ]
        return Response(data)