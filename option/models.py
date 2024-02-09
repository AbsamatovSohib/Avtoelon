from django.db import models
from utils.models import BaseModel


# Create your models here.
class OptionType(models.TextChoices):
    SINGLE = "Single"
    EXTENDED = "Extended"
    CHOICE = "Choice"
    BUTTON = "Button"
    TEXT = "Text"
    NUMBER = "Number"
    MULTIPLE_CHOICE = "Multiple choice"


class Option(BaseModel):
    title = models.CharField(max_length=256)  # Марка и модель, Кузов , Объём двигателя
    type = models.CharField(max_length=15, choices=OptionType.choices)
    code = models.CharField(
        max_length=256, null=True, blank=True
    )  # year, bargain,auto_car_transm,auto-run

    is_main = models.BooleanField(default=False)
    is_filter = models.BooleanField(default=False)
    is_main_filter = models.BooleanField(default=False)
    is_advanced_filter = models.BooleanField(default=False)

    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class OptionValue(BaseModel):
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="values")
    value = models.CharField(max_length=256)  # Bentley, Sedan, Zadniy

    def __str__(self):
        return self.value


class OptionValueExtended(BaseModel):
    option_value = models.ForeignKey(
        OptionValue,
        on_delete=models.CASCADE,
        related_name="values_extended",
    )
    value = models.CharField(max_length=256)  # Continental
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )

    def __str__(self):
        return self.value


class PostOption(BaseModel):
    post = models.ForeignKey(
        "avto.Post", on_delete=models.CASCADE, related_name="options"
    )
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="posts")
    value = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f"{self.post} {self.option}"


class PostOptionValue(BaseModel):
    post_option = models.ForeignKey(
        PostOption, on_delete=models.CASCADE, related_name="values"
    )
    option_value = models.ForeignKey(OptionValue, on_delete=models.CASCADE)
    option_value_extended = models.ForeignKey(
        OptionValueExtended, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        unique_together = ("post_option", "option_value")
