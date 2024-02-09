from django.db import models
from utils.models import BaseModel


class Region(BaseModel):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class District(BaseModel):
    title = models.CharField(max_length=256)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="districts"
    )

    is_filter = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# Create your models here.
class Category(BaseModel):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class SubCategory(BaseModel):
    title = models.CharField(max_length=256)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )
    has_price = models.BooleanField(default=True)
    options = models.ManyToManyField(
        "option.Option",
    )

    def __str__(self):
        return self.title


class Post(BaseModel):
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name="posts"
    )

    published_at = models.DateTimeField(auto_now_add=True)
    info = models.TextField(blank=True, null=True)
    price = models.IntegerField(default=0, null=True, blank=True)
    views = models.IntegerField(default=0, editable=False)
    main_photo = models.ImageField(blank=True, null=True, editable=False)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="posts"
    )
    json = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.info
        
    def make_json_fields(self):
        post_options = self.options.all()
        data = {
            "title": "",
            "extended_title": "",
            "year": "",
            "model": "",
            "district": "",
            "photos_count": 0,
            "options": [],
        }
        for post_option in post_options:
            data["options"].append(
                {
                    "title": post_option.option.title,
                    "value": post_option.value,
                    "values": [
                        values.option_value.value for values in post_option.values.all()
                    ],
                }
            )
            if post_option.option.code == "year":
                data["year"] = post_option.value
            if post_option.option.code == "model":
                for value in post_option.values.all():
                    if value.option_value_extended:
                        parent = ""
                        if value.option_value_extended.parent:
                            data["model"] = (
                                f"{value.option_value.value} {value.option_value_extended.parent.value}, {value.option_value_extended.value}"
                            )
                        else:
                            data["model"] = (
                                f"{value.option_value.value} {value.option_value_extended.value}"
                            )
                    else:
                        data["model"] = value.option_value.value

        data["district"] = self.district.title
        data["photos_count"] = self.photos.count()
        data["title"] = f"{data['model']}"
        data["extended_title"] = f"{data['model']} {data['year']} {self.price}  y.e."
        return data


class Photo(BaseModel):
    image = models.ImageField(upload_to="photos")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="photos")
    is_main = models.BooleanField(default=False)

    @classmethod
    def get_main_photo(cls, post_id):
        photo = Photo.objects.filter(post_id=post_id, is_main=True).first()
        print(photo)
        if photo:
            return photo.image
        return None
