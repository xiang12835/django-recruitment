# Register your models here.

from django.contrib import admin
from django.http import HttpResponse
from datetime import datetime
import logging
import csv
from django.db.models import Q
from interview.models import Candidate
from job.models import Resume
from libs.bot import dingtalk
from django.utils.safestring import mark_safe
from .tasks import send_dingtalk_message

logger = logging.getLogger(__name__)

exportable_fields = ('username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result', 'first_interviewer_user',
                     'second_result', 'second_interviewer_user', 'hr_result', 'hr_score', 'hr_remark', 'hr_interviewer_user')

# 通知一面面试官面试
def notify_interviewer(modeladmin, request, queryset):
    candidates = ""
    interviewers = ""
    for obj in queryset:
        candidates = obj.username + ";" + candidates
        interviewers = obj.first_interviewer_user.username + ";" + interviewers
    # 这里的消息发送到钉钉， 或者通过 Celery 异步发送到钉钉
    # dingtalk.send ("候选人 %s 进入面试环节，亲爱的面试官，请准备好面试： %s" % (candidates, interviewers) )
    # dingtalk.send("@%s，睡麻痹起来嗨！" % candidates)
    # 使用celery异步调用，通知面试
    send_dingtalk_message.delay("@%s，睡麻痹起来嗨！" % candidates)
    # messages.add_message(request, messages.INFO, '已经成功发送面试通知')


notify_interviewer.short_description = u'通知一面面试官'

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
export_model_as_csv.allowed_permissions = ('export',)


# 候选人管理类
class CandidateAdmin(admin.ModelAdmin):

    actions = (export_model_as_csv, notify_interviewer,)

    # 导出功能权限：当前用户是否有导出权限：
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "export"))

    # 排除一些属性，此时数据库也会没有
    exclude = ('creator', 'created_date', 'modified_date')

    # list_display  # 列表页中的字段展示
    list_display = (
            'username', 'city', 'bachelor_school', 'get_resume','first_score', 'first_result', 'first_interviewer_user', 'second_score',
            'second_result', 'second_interviewer_user', 'hr_score', 'hr_result', 'hr_interviewer_user',)

    # 右侧筛选条件
    list_filter = (
    'city', 'first_result', 'second_result', 'hr_result', 'first_interviewer_user', 'second_interviewer_user',
    'hr_interviewer_user')

    # 查询字段
    search_fields = ('username', 'phone', 'email', 'bachelor_school')

    # 列表页排序字段
    ordering = ('hr_result', 'second_result', 'first_result',)

    def get_resume(self, obj):  # 列表页中的字段展示，还可以列表页中的引用方法来展示
        if not obj.phone:
            return ""
        resumes = Resume.objects.filter(phone=obj.phone)
        if resumes and len(resumes) > 0:
            return mark_safe(u'<a href="/resume/%s" target="_blank">%s</a' % (resumes[0].id, "查看简历"))
        return ""

    get_resume.short_description = '查看简历'
    get_resume.allow_tags = True

    # 分组展示字段，分三块，基础信息、第一轮面试记录、第二轮面试（专业复试）、HR复试
    # 字段合并操作，从一行到多行的展示，在一行里展示多个字段，直接加刮号
    default_fieldsets = (
        (None, {'fields': (
            "userid", ("username", "city", "phone"),
            ("email", "apply_position", "born_address", "gender", "candidate_remark"),
            ("bachelor_school", "master_school", "doctor_school"), ("major", "degree"), "test_score_of_general_ability",
            "paper_score",)}),
        ('第一轮面试', {'fields': (
            ("first_score", "first_learning_ability", "first_professional_competency"), "first_advantage",
            "first_disadvantage",
            "first_result", "first_recommend_position", "first_interviewer_user", "first_remark",)}),
        ('第二轮面试（专业复试）', {'fields': ("second_score", ("second_learning_ability", "second_professional_competency"), (
            "second_pursue_of_excellence", "second_communication_ability", "second_pressure_score"), "second_advantage",
                                    "second_disadvantage", "second_result", "second_recommend_position",
                                    "second_interviewer_user", "second_remark",)}),
        ('HR复试', {'fields': (
            "hr_score", ("hr_responsibility", "hr_communication_ability", "hr_logic_ability"),
            ("hr_potential", "hr_stability"),
            "hr_advantage", "hr_disadvantage", "hr_result", "hr_interviewer_user", "hr_remark",)}),
    )

    default_fieldsets_first = (
        (None, {'fields': ("userid", ("username", "city", "phone"),
                           ("email", "apply_position", "born_address", "gender", "candidate_remark"),
                           ("bachelor_school", "master_school", "doctor_school"), ("major", "degree"),
                           "test_score_of_general_ability", "paper_score",)}),
        ('第一轮面试', {'fields': (
            ("first_score", "first_learning_ability", "first_professional_competency"), "first_advantage",
            "first_disadvantage", "first_result", "first_recommend_position", "first_interviewer_user",
            "first_remark",)}),
    )

    default_fieldsets_second = (
        (None, {'fields': ("userid", ("username", "city", "phone"),
                           ("email", "apply_position", "born_address", "gender", "candidate_remark"),
                           ("bachelor_school", "master_school", "doctor_school"), ("major", "degree"),
                           "test_score_of_general_ability", "paper_score",)}),
        ('第一轮面试', {'fields': (
            ("first_score", "first_learning_ability", "first_professional_competency"), "first_advantage",
            "first_disadvantage", "first_result", "first_recommend_position", "first_interviewer_user",
            "first_remark",)}),
        ('第二轮面试（专业复试）', {'fields': ("second_score", ("second_learning_ability", "second_professional_competency"), (
            "second_pursue_of_excellence", "second_communication_ability", "second_pressure_score"), "second_advantage",
                                    "second_disadvantage", "second_result", "second_recommend_position",
                                    "second_interviewer_user", "second_remark",)}),
    )

    # 数据权限：一面面试官仅填写一面反馈， 二面面试官可以填写二面反馈
    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return self.default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return self.default_fieldsets_second
        return self.default_fieldsets

    # 数据集的权限：对于非管理员，非HR，获取自己是一面面试官或者二面面试官的候选人集合:s
    def get_queryset(self, request):  # show data only owned by the user
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return Candidate.objects.filter(
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user))

    # 设置字段只读
    # readonly_fields = ("first_interviewer_user", "second_interviewer_user",)

    # 需要让hr登录能够修改面试官下拉选择，而面试官登录需要只读
    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names

    def get_readonly_fields(self, request, obj):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return ('first_interviewer_user', 'second_interviewer_user',)
        return ()

    # 让 hr 登录后，在列表页就可以修改面试官，提高工作效率。面试官不让修改
    # list_editable = ('first_interviewer_user','second_interviewer_user',)
    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or 'hr' in group_names:
            return ('first_interviewer_user', 'second_interviewer_user',)
        return ()

    def get_changelist_instance(self, request):
        """
        override admin method and list_editable property value
        with values returned by our custom method implementation.
        """
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    def save_model(self, request, obj, form, change):
        # 在保存模型之前做一些操作，会被自动调用
        obj.last_editor = request.user.username
        if not obj.creator:
            obj.creator = request.user.username
        obj.modified_date = datetime.now()
        obj.save()


admin.site.register(Candidate, CandidateAdmin)

