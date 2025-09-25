from django.db import models 

# Create your models here.
class Doc(models.Model):  
    uploadfile = models.FileField(upload_to='media', default='please upload file')
    title = models.CharField(max_length=50, default='Welcome')
    class Meta:  
        db_table = "Document"  

    def __str__(self):
        return self.title