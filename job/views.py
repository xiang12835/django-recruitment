from django.http import Http404
from django.shortcuts import render
from job.models import Job

import logging

logger = logging.getLogger(__name__)

# Create your views here.

def job_list(request):
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

