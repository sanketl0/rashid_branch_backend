from django.db import models
from salescustomer.BaseModel import *
import uuid
from company.models import Company, Branch,Company_Year


EXT_TYPE = (
    ('TALLY','TALLY'),
)

STATUS = (
    ('IDLE','IDLE'),
    ('PROCESSING','PROCESSING'),
    ('FAILED', 'FAILED'),
    ('COMPLETED','COMPLETED')
)
APP = (
    ('LOCAL','LOCAL'),
    ('CLOUD','CLOUD'),

)


class VersionHelper(BaseDateid):
    name = models.CharField(max_length=50,blank=True,null=True)
    version = models.CharField(max_length=50,blank=True,null=True)
    version_type= models.CharField(max_length=50,blank=True,null=True)
    isDeprecated=models.BooleanField(default=False)
    file = models.FileField(upload_to='patches/',blank=True,null=True)

class Task(BaseDateid):
    task_id =  models.UUIDField(primary_key=True, default=uuid.uuid4)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    company_yearid = models.ForeignKey(Company_Year, on_delete=models.SET_NULL, null=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    ref_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    module = models.CharField(max_length=50, blank=True, null=True)
    filter = models.JSONField(default=dict)
    message =  models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    retried = models.PositiveIntegerField(default=0)
    ext_type = models.CharField(max_length=50, default='TALLY', choices=EXT_TYPE)
    domain_name=models.CharField(max_length=200, blank=True,null=True)
    client_domain_name=models.CharField(max_length=200,blank=True,null=True)
    application = models.CharField(max_length=200, default='LOCAL', choices=APP)
    db_name = models.CharField(max_length=200,blank=True,null=True)
    class Meta:
        ordering = ['-created_date']


class TaskLogs(BaseDateid):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE,blank=True,null=True)
    message = models.TextField(blank=True, null=True)
    error = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date']

