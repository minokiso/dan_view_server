from django.db import models


# Create your models here.
class LastDayOutPut(models.Model):
    status = models.IntegerField(null=True, default=1)
    time = models.DateTimeField(null=True)
    value = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'last_day_out_put'


class RealOEEDay(models.Model):
    status = models.IntegerField(null=True, default=1)
    time = models.DateTimeField(null=True)
    value = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'real_oeeday'
