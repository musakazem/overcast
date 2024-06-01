from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    creator = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_creator",
    )
    archived = models.BooleanField(default=False)

    class Meta:
        abstract = True
