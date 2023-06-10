import uuid
from django.core.exceptions import ValidationError, PermissionDenied

from django.apps import apps
from django.db import models
from django.db.models import Max
from user_manager.models import User


class Memo(models.Model):
    name = models.TextField(null=True, blank=True, default=None)
    created_at = models.DateField(auto_now_add=True)

    # TODO  note: might have to add owner field
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)


class MemoItem(models.Model):
    parent_memo = models.ForeignKey(
        Memo, on_delete=models.CASCADE, related_name="memo_items"
    )
    is_completed = models.BooleanField(default=False)
    description = models.TextField()
    order = models.SmallIntegerField(default=-1)

    def save(self, **kwargs):
        if (
            MemoItem.objects.filter(parent_memo=self.parent_memo, order=self.order)
            .exclude(id=self.id)
            .exists()
        ):
            reorder_item = (
                MemoItem.objects.filter(
                    parent_memo=self.parent_memo, order__gte=self.order
                )
                .exclude(id=self.id)
                .order_by("-order")
            )
            for instance in reorder_item:
                instance.order += 1
                instance.save()
        if self.order == -1:
            max_value = (
                MemoItem.objects.filter(parent_memo=self.parent_memo)
                .exclude(id=self.id)
                .aggregate(max_order=Max("order"))["max_order"]
                or 0
            )
            self.order = max_value + 1
        super().save(**kwargs)

    def delete(self, **kwargs):
        reorder_item = MemoItem.objects.filter(
            parent_memo=self.parent_memo, order__gt=self.order
        ).order_by("order")
        super().delete(**kwargs)
        for instance in reorder_item:
            instance.order -= 1
            instance.save()
