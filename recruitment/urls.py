"""recruitment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _


urlpatterns = [

    # 职位管理 url
    path("", include("job.urls")),

    # grappelli 风格主题 url
    path('grappelli/', include('grappelli.urls')),

    # 多语言
    path('i18n/', include('django.conf.urls.i18n')),

    # 后台管理系统 url
    path('admin/', admin.site.urls),

    # 候选人注册登录 url
    path('accounts/', include('registration.backends.simple.urls')),

]


admin.site.site_header = _('匠果科技招聘管理系统')
