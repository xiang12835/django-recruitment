from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.contrib import messages
from job.models import Job, Resume
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required, login_required

import logging

logger = logging.getLogger(__name__)

# Create your views here.

def job_list(request): # 方法视图
    job_list = Job.objects.order_by('job_type')
    context =  {'job_list': job_list}
    for job in job_list:
        job.city_name = Job.Cities[job.job_city][1]
        job.type_name = Job.JobTypes[job.job_type][1]
    return render(request, 'job_list.html', context)


def job_detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Job.Cities[job.job_city][1]
        logger.info('job retrieved from db :%s' % job_id)
    except Job.DoesNotExist:
        raise Http404("Job does not exist")
    return render(request, 'job_detail.html', {'job': job})

# 这个 URL 仅允许有 创建用户权限的用户访问
# @csrf_exempt # 去掉这个装饰器，解决csrf问题
@permission_required('auth.user_add')
def create_hr_user(request):
    if request.method == "GET":
        return render(request, 'create_hr.html', {})
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        hr_group = Group.objects.get(name='hr') 
        user = User(is_superuser=False, username=username, is_active=True, is_staff=True)
        user.set_password(password)
        user.save()
        user.groups.add(hr_group)

        messages.add_message(request, messages.INFO, 'user created %s' % username)
        return render(request, 'create_hr.html')
    return render(request, 'create_hr.html')

'''
直接返回  HTML 内容的视图 （这段代码返回的页面有 XSS 漏洞，能够被攻击者利用）
'''
def detail_resume(request, resume_id):
    try:
        resume = Resume.objects.get(pk=resume_id)
        content = "name: %s <br>  introduction: %s <br>" % (resume.username, resume.candidate_introduction)
        # return HttpResponse(content) # 有 XSS 漏洞 
        return HttpResponse(html.escape(content)) # 解决
    except Resume.DoesNotExist:
        raise Http404("resume does not exist")

class ResumeDetailView(DetailView):
    """   简历详情页    """
    model = Resume
    template_name = 'resume_detail.html'

class ResumeCreateView(LoginRequiredMixin, CreateView): # 简历的创建视图，是一个类视图
    """    简历职位页面  """
    template_name = 'resume_form.html'
    success_url = '/job_list/'
    model = Resume
    fields = ["username", "city", "phone",
        "email", "apply_position", "gender",
        "bachelor_school", "master_school", "major", "degree", "picture", "attachment",
        "candidate_introduction", "work_experience", "project_experience"]

    def post(self, request, *args, **kwargs):
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            # <process form cleaned data>
            form.save()
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})


    ### 从 URL 请求参数带入默认值
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.applicant = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
