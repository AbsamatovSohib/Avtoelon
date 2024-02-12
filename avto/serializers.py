from rest_framework import serializers
from avto.models import Post,District
from option.serializers import PostOptionSerializer


class PostSerializer(serializers.ModelSerializer):
    district = serializers.StringRelatedField(source="json.district")
    title = serializers.StringRelatedField(source="json.title", read_only=True)
    extended_title = serializers.StringRelatedField(
        source="json.extended_title", read_only=True
    )
    photo_count = serializers.IntegerField(source="json.photos_count", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "extended_title",
            "photo_count",
            "main_photo",
            "district",
        )
        
class PostSerializer(serializers.ModelSerializer):
    district = serializers.StringRelatedField(source="json.district")
    title = serializers.StringRelatedField(source="json.title", read_only=True)
    extended_title = serializers.StringRelatedField(
        source="json.extended_title", read_only=True
    )
    photo_count = serializers.IntegerField(source="json.photos_count", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "extended_title",
            "photo_count",
            "main_photo",
            "district",
        )

class StatisticBuyCarSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    def get_post_count(self, district):
        return district.post_set.count()

    class Meta:
        model = District
        fields = ['id', 'name', 'post_count']