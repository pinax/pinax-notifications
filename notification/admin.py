from django.contrib import admin

from notification.models import NoticeType, NoticeSetting, Notice, NoticeQueueBatch


class NoticeTypeAdmin(admin.ModelAdmin):
    list_display = ["label", "display", "description", "default"]


class NoticeSettingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "notice_type", "medium", "send"]


class NoticeAdmin(admin.ModelAdmin):
    list_display = ["message", "recipient", "sender", "notice_type", "added", "unseen", "archived"]


admin.site.register(NoticeQueueBatch)
admin.site.register(NoticeType, NoticeTypeAdmin)
admin.site.register(NoticeSetting, NoticeSettingAdmin)
admin.site.register(Notice, NoticeAdmin)
