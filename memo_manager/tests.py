from rest_framework import status
from rest_framework.test import APITestCase
from user_manager.models import User
from memo_manager.models import Memo, MemoItem
from django.urls import reverse
from datetime import datetime
from datetime import timedelta
from django.utils import timezone

import pytz


class WorkOrderTestCase(APITestCase):
    # def given_user(self, user):
    #     self.current_user = user
    #     self.client.force_login(user)

    def user_gets(self, url):
        self.response = self.client.get(url, format="json")
        self.response_json = self.response.json()
        return self.response_json

    def user_posts(self, url, data, format="json"):
        self.response = self.client.post(url, data, format)
        self.response_json = self.response.json()
        return self.response_json

    def user_put(self, url, data, format="json"):
        self.response = self.client.put(url, data, format)
        self.response_json = self.response.json()
        return self.response_json

    def user_patch(self, url, data, format="json"):
        self.response = self.client.patch(url, data, format)
        self.response_json = self.response.json()
        return self.response_json

    def user_delete(self, url):
        self.response = self.client.delete(url, format="json")
        return self.response

    def test_get_memo(self):
        memo = Memo.objects.create(
            name="test",
        )
        MemoItem.objects.create(
            parent_memo=memo, description="create application with react and django "
        )
        self.user_gets(url="/memo/")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_get_memoitem(self):
        memo = Memo.objects.create(
            name="test",
        )
        MemoItem.objects.create(
            parent_memo=memo, description="create application with react and django "
        )
        self.user_gets(url=f"/memo/{memo.id}/item/")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_post_memo(self):
        now = datetime.now(pytz.timezone("UTC"))
        self.user_posts(
            url=f"/memo/",
            data={"name": "test2", "reminder_at": now},
        )
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_patch_memo(self):
        memo = Memo.objects.create(
            name="test",
        )

        self.user_patch(
            url=f"/memo/{memo.id}/",
            data={"name": "test2", "items": [{"description": "test2"}]},
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_post_memo_item(self):
        memo = Memo.objects.create(name="test")
        MemoItem.objects.create(
            parent_memo=memo, description="create application with react and django "
        )
        self.user_posts(url=f"/memo/{memo.id}/item/", data={"description": "test2"})
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.user_gets(url=f"/memo/{memo.id}/item/")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.response_json), 2)
        for i, res in enumerate(self.response_json):
            self.assertEqual(res["order"], i + 1)

    def test_patch_memo_item(self):
        memo = Memo.objects.create(name="test")
        MemoItem.objects.create(
            parent_memo=memo, description="create application with react and django "
        )
        memo_item = MemoItem.objects.create(
            parent_memo=memo, description="target_memo_item"
        )
        self.user_patch(
            url=f"/memo/{memo.id}/item/{memo_item.id}/",
            data={"is_completed": True, "order": 1},
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

        self.user_gets(url=f"/memo/{memo.id}/item/")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        for i, res in enumerate(self.response_json):
            self.assertEqual(res["order"], i + 1)
        self.assertEqual(self.response_json[0]["is_completed"], True)
        self.assertEqual(self.response_json[0]["description"], memo_item.description)

    def test_delete_memo_item(self):
        memo = Memo.objects.create(name="test")
        memo_item = MemoItem.objects.create(
            parent_memo=memo, description="create application with react and django "
        )
        MemoItem.objects.create(parent_memo=memo, description="target_memo_item_1")
        MemoItem.objects.create(parent_memo=memo, description="target_memo_item_2")
        self.user_delete(
            url=f"/memo/{memo.id}/item/{memo_item.id}/",
        )
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

        self.user_gets(url=f"/memo/{memo.id}/item/")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.response_json), 2)
        for i, res in enumerate(self.response_json):
            self.assertEqual(res["order"], i + 1)
            self.assertEqual(res["description"], f"target_memo_item_{i + 1}")
