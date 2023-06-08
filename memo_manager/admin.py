from memo_manager.models import Memo, MemoItem
from django.contrib.admin import AdminSite, TabularInline, StackedInline
from django.contrib import admin


class MemoAdmin(admin.ModelAdmin):
    model = Memo
    fields = [
        field.name
        for field in Memo._meta.fields
        if field.name not in ["id", "created_at"]
    ]
    list_display = fields


class MemoItemAdmin(admin.ModelAdmin):
    model = MemoItem
    fields = [field.name for field in MemoItem._meta.fields if field.name not in ["id"]]
    list_display = fields


admin.site.register(Memo, MemoAdmin)
admin.site.register(MemoItem, MemoItemAdmin)
