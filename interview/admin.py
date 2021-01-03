from datetime import datetime

from django.contrib import admin

# Register your models here.
from interview.models import Candidate

# 候选人管理类
class CandidateAdmin(admin.ModelAdmin):

    # 排除一些属性，此时数据库也会没有
    exclude = ('creator', 'created_date', 'modified_date')

    # list_display  # 列表页中的字段展示
    list_display = (
            'username', 'city', 'bachelor_school','first_score', 'first_result', 'first_interviewer_user', 'second_score',
            'second_result', 'second_interviewer_user', 'hr_score', 'hr_result', 'hr_interviewer_user',)

    # 使用fieldsets进行分组，分组显示字段，
    # 分三块，基础信息、第一轮面试记录、第二轮面试（专业复试）、HR复试
    # fieldsets = (
    #     (None, {'fields': ('userid', 'username',)}),
    #     ('分组一', {'fields': ('', '',)}),
    #     ('分组二', {'fields': ('', '',)}),
    # )

    # 右侧筛选条件
    list_filter = (
    'city', 'first_result', 'second_result', 'hr_result', 'first_interviewer_user', 'second_interviewer_user',
    'hr_interviewer_user')

    # 查询字段
    search_fields = ('username', 'phone', 'email', 'bachelor_school')

    # 列表页排序字段
    ordering = ('hr_result', 'second_result', 'first_result',)

    def save_model(self, request, obj, form, change):
        # 在保存模型之前做一些操作，会被自动调用
        obj.last_editor = request.user.username
        if not obj.creator:
            obj.creator = request.user.username
        obj.modified_date = datetime.now()
        obj.save()


admin.site.register(Candidate, CandidateAdmin)

