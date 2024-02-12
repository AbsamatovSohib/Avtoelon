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
        districts = District.objects.annotate(post_count=Count('posts'))
        data = [
            {
            'region_name': district.title,
            'post_count': district.post_count
        } for district in districts
        ]
        return Response(data)