from django.contrib import admin

# Register your models here.
from interview.models import Candidate

# 候选人管理类
class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')


admin.site.register(Candidate, CandidateAdmin)

