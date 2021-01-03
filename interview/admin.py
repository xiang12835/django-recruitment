# Register your models here.

from django.contrib import admin
from django.http import HttpResponse
from datetime import datetime
import logging
import csv

from interview.models import Candidate

logger = logging.getLogger(__name__)

exportable_fields = ('username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result', 'first_interviewer_user',
                     'second_result', 'second_interviewer_user', 'hr_result', 'hr_score', 'hr_remark', 'hr_interviewer_user')


# define export action
def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=%s-list-%s.csv' % (
        'recruitment-candidates',
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    # 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list],
    )

    for obj in queryset:
        ## 单行 的记录（各个字段的值）， 根据字段对象，从当前实例 (obj) 中获取字段值
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)
    logger.error(" %s has exported %s candidate records" % (request.user.username, len(queryset)))

    return response


export_model_as_csv.short_description = u'导出为CSV文件'

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

