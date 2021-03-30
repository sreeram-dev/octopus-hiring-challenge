# -*-coding:utf-8-*-

from django.db import models


class MeterReading(models.Model):
    """Model for storing meter reading in a database
    Model Specification available at
    https://www.aemo.com.au/-/media/Files/Electricity/NEM/Retail_and_Metering/Metering-Procedures/2018/MDFF-Specification-NEM12--NEM13-v106.pdf
    Pageno: 13
    """
    nmi = models.CharField(max_length=10)
    meter_serial_number = models.CharField(max_length=12)
    reading_value = models.CharField(max_length=13)
    reading_time = models.DateTimeField()
    # Django Filefield has a default limitation of 100 chars, following it here
    filename = models.CharField(max_length=100)
