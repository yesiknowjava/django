from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
LEAVE_TYPE = ((1, _("PL")), (2, _("SL")), (3, _("CL")), (4, _("Comp Off")))
LEAVE_STATUS = ((1, _("Pending")),(2, _("Approved")), (3, _("Rejected")))
# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    manager = models.BooleanField(default=False)
    def __str__(self):
        return self.first_name + " " + self.last_name


class Leave(models.Model):
    requester = models.ForeignKey("sslmsapp.Employee", related_name='requester', verbose_name=_("Requester"), on_delete=models.CASCADE)
    approver = models.ForeignKey("sslmsapp.Employee", related_name='approver', verbose_name=_("Approver"), on_delete=models.CASCADE)
    reason = models.TextField()
    leave_type = models.IntegerField(choices=LEAVE_TYPE, default=1)
    leave_status = models.IntegerField(choices=LEAVE_STATUS, default=1)
    start_date = models.DateField(_("Start Date"), auto_now=False, auto_now_add=False)
    end_date = models.DateField(_("End Date"), auto_now=False, auto_now_add=False)
    def __str__(self):
        return self.requester.first_name + " " + self.requester.last_name