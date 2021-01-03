from django.contrib import admin

# Register your models here.
from interview.models import Candidate

# 候选人管理类
class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')
    list_display = (
            'username', 'city', 'bachelor_school','first_score', 'first_result', 'first_interviewer_user', 'second_score',
            'second_result', 'second_interviewer_user', 'hr_score', 'hr_result', 'hr_interviewer_user',)

    # 使用fieldsets进行分组
    # fieldsets = (
    #     (None, {'fields': ('userid', 'username',)}),
    #     ('分组一', {'fields': ('', '',)}),
    #     ('分组二', {'fields': ('', '',)}),
    # )


admin.site.register(Candidate, CandidateAdmin)

