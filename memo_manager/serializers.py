from django.core.exceptions import ValidationError
from rest_framework import serializers
from memo_manager.models import Memo, MemoItem


class MemoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoItem
        fields = ["id", "is_completed", "description", "order"]
        read_only = ["id"]
        ordering = [
            "order",
        ]

    def create(self, validated_data):
        validated_data["parent_memo"] = self.context["parent_memo"]
        return super().create(validated_data)

    def reorder_other_item(self, target_order, current_order, parent_memo):
        if current_order < target_order:
            decrease_reorder_item = MemoItem.objects.filter(
                parent_memo=parent_memo,
                order__gt=current_order,
                order__lte=target_order,
            ).order_by("-order")
            for instance in decrease_reorder_item:
                instance.order -= 1
                instance.save()
        else:
            if MemoItem.objects.filter(
                parent_memo=parent_memo, order=target_order
            ).exists():
                increase_reorder_item = MemoItem.objects.filter(
                    parent_memo=parent_memo, order__gte=target_order
                ).order_by("-order")
                for instance in increase_reorder_item:
                    instance.order += 1
                    instance.save()

    def update(self, instance, validated_data):
        self.reorder_other_item(
            target_order=validated_data["order"],
            current_order=instance.order,
            parent_memo=instance.parent_memo,
        )

        return super().update(instance, validated_data)


class ReOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoItem
        fields = ["id", "is_completed", "description", "order"]
        read_only = ["id", "is_completed", "description"]
        ordering = [
            "order",
        ]


class MemoSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Memo

        fields = ["id", "name", "created_at", "items"]
        read_only = [
            "created_at",
        ]
        ordering = ["created_at", "item"]

    def get_items(self, obj):
        return MemoItemSerializer(
            MemoItem.objects.filter(parent_memo=obj).order_by("order"), many=True
        ).data
