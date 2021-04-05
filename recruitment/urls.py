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

from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
from job.models import Job


# https://www.django-rest-framework.org/

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'jobs', JobViewSet)

urlpatterns = [

    # 职位管理 url
    path("", include("job.urls")),

    # django rest api & api auth (login/logout)
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),

    # grappelli 风格主题 url
    path('grappelli/', include('grappelli.urls')),

    # 多语言
    path('i18n/', include('django.conf.urls.i18n')),

    # 后台管理系统 url
    path('admin/', admin.site.urls),

    # 候选人注册登录 url
    path('accounts/', include('registration.backends.simple.urls')),

]

from django.conf.urls import include, url
from django.conf import settings

from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = _('匠果科技招聘管理系统')
