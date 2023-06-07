import uuid
from django.core.exceptions import ValidationError, PermissionDenied

from django.apps import apps
from django.db import models

from user_manager.models import User


class Memo(models.Model):
    name = models.TextField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    reminder_at = models.DateTimeField()
    # TODO  note: might have to add owner field
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)


class MemoItem(models.Model):
    parent_memo = models.ForeignKey(Memo, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)
    description = models.TextField()
