from django.core.exceptions import ValidationError
from rest_framework import serializers
from memo_manager.models import Memo, MemoItem


class MemoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoItem
        fields = ["id", "is_completed", "description", "order"]
        ordering = [
            "order",
        ]

    def create(self, validated_data):
        validated_data["parent_memo"] = self.context["parent_memo"]
        return super().create(validated_data)


class MemoSerializer(serializers.ModelSerializer):
    items = MemoItemSerializer(many=True, source="memo_items", read_only=True)

    class Meta:
        model = Memo

        fields = ["id", "name", "created_at", "reminder_at", "items"]
        read_only = [
            "created_at",
        ]
        ordering = [
            "reminder_at",
        ]
