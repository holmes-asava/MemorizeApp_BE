from rest_framework import mixins, viewsets

from config.permissions import *
from memo_manager.models import Memo, MemoItem
from memo_manager.serializers import MemoSerializer, MemoItemSerializer


class MemoViewset(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
    permission_classes = [AllowAny]

    # TODO might have to add get_queryset to return only own memo
    # def get_queryset(self):
    #     if self.request.user.is_guest:
    #         return self.queryset.filter(created_by=self.request.user)
    #     return self.queryset
