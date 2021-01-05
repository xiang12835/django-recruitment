from django.conf.urls import url
from django.urls import path
from django.conf import settings

from job import views


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    # 职位列表
    path("job_list/", views.job_list, name="job_list"),

    # 管理员创建 HR 账号的 页面:
    # path('create_hr_user/', views.create_hr_user, name='create_hr_user'),

    # 职位详情
    url(r'^job_detail/(?P<job_id>\d+)/$', views.job_detail, name='detail'),
    # path('job_detail/<int:job_id>/', views.detail, name='job_detail'),

    # 简历提交
    path('resume/add/', views.ResumeCreateView.as_view(), name='resume-add'),
    # 简历详情
    path('resume/<int:pk>/', views.ResumeDetailView.as_view(), name='resume-detail'),

    # path('sentry-debug/', trigger_error),

    # 首页自动跳转到 职位列表
    url(r"^$", views.job_list, name="name"),
    # path("", views.job_list, name="name"),

]