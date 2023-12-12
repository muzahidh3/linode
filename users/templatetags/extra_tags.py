from django import template
register = template.Library()  
from users.models import CcnJobCard


# For Admin Dashboard
@register.filter
def TotalPendingJob(self):
    total_pending_job = CcnJobCard.objects.filter(job_on="CCN Head").count()
    return("{:,}".format(total_pending_job))

@register.filter
def TotalJob(self):
    total_job = CcnJobCard.objects.filter(status=False).count()
    return("{:,}".format(total_job))


