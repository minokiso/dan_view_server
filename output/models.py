from django.db import models


# Create your models here.
class LastDayOutPut(models.Model):
    status = models.IntegerField(null=True, default=1)
    time = models.DateTimeField(null=True)
    value = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'last_day_out_put'
        ordering = ('-time',)


class RealOEEDay(models.Model):
    status = models.IntegerField(null=True, default=1)
    time = models.DateTimeField(null=True)
    value = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'real_oeeday'
        ordering = ('-time',)


class EVR1(models.Model):
    time = models.DateTimeField(null=True)
    value = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'evr1'
        ordering = ('-time',)


class EVR2(models.Model):
    time = models.DateTimeField(null=True)
    value = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'evr2'
        ordering = ('-time',)
