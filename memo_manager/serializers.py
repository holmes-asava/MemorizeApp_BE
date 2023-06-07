from django.core.exceptions import ValidationError
from rest_framework import serializers
from memo_manager.models import Memo, MemoItem


class MemoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoItem

        fields = ["is_complete", "description"]


class MemoSerializer(serializers.ModelSerializer):
    items = MemoItemSerializer(many=True, source="memo_items")

    class Meta:
        model = Memo

        fields = ["id", "name", "created_at", "reminder_at", "items"]
        read_only = [
            "created_at",
        ]
