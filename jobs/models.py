from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Job(models.Model):
    JobTypes = [
        (0, "技术类"),
        (1, "产品类"),
        (2, "运营类"),
        (3, "设计类"),
        (4, "市场营销类")
    ]

    Cities = [
        (0, "北京"),
        (1, "上海"),
        (2, "深圳"),
        (3, "杭州"),
        (4, "广州")
    ]

    # Translators: 职位实体的翻译
    job_type = models.SmallIntegerField(blank=False, choices=JobTypes, verbose_name=_("职位类别"))
    job_name = models.CharField(max_length=250, blank=False, verbose_name=_("职位名称"))
    job_city = models.SmallIntegerField(choices=Cities, blank=False, verbose_name=_("工作地点"))
    job_responsibility = models.TextField(max_length=1024, verbose_name=_("职位职责"))
    job_requirement = models.TextField(max_length=1024, blank=False, verbose_name=_("职位要求"))
    creator = models.ForeignKey(User, verbose_name=_("创建人"), null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(verbose_name=_("创建日期"), auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name=_("修改日期"), auto_now=True)

    class Meta:
        verbose_name = _('职位')
        verbose_name_plural = _('职位列表')

    def __str__(self):
        return self.job_name
