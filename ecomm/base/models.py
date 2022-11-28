from django.db import models



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now= True)
    created_by = models.CharField(max_length=255, default='dj')
    updated_at = models.DateTimeField(auto_now_add= True)
    updated_by = models.CharField(max_length=255, default='dj')


    class Meta:
        abstract = True