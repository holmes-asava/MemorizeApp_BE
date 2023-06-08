from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from config.permissions import *
from memo_manager.models import Memo, MemoItem
from memo_manager.serializers import MemoSerializer, MemoItemSerializer


class MemoViewset(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Memo.objects.all()
    serializer_class = MemoSerializer
    permission_classes = [AllowAny]

    @action(methods=["GET", "POST"], detail=True, serializer_class=MemoItemSerializer)
    def item(self, request, pk, *args, **kwargs):
        memo = get_object_or_404(self.get_queryset(), id=pk)
        if request.method == "GET":
            serializer = self.get_serializer(
                MemoItem.objects.filter(parent_memo=memo).order_by("order"), many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            serializer = self.get_serializer(
                data=request.data, context={"parent_memo": memo}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(methods=["PUT", "DELETE"])
    @action(
        methods=["PATCH", "DELETE"],
        detail=True,
        serializer_class=MemoItemSerializer,
        url_path="item/(?P<memo_item_id>\d+)",
    )
    def patch_or_delete_item(self, request, pk, memo_item_id, *args, **kwargs):
        memo = get_object_or_404(Memo, id=pk)
        memo_item = get_object_or_404(MemoItem, id=memo_item_id, parent_memo=memo)
        if request.method == "DELETE":
            memo_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        elif request.method == "PATCH":
            serializer = self.get_serializer(memo_item, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )


# TODO might have to add get_queryset to return only own memo
# def get_queryset(self):
#     if self.request.user.is_guest:
#         return self.queryset.filter(created_by=self.request.user)
#     return self.queryset
# class MemoItemViewset(
#     viewsets.GenericViewSet,
#     mixins.ListModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
# ):
