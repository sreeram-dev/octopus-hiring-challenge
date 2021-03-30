from django.contrib import admin
from meter.models import MeterReading


class MeterReadingAdmin(admin.ModelAdmin):
    list_display = ('nmi', 'meter_serial_number',
                    'reading_value', 'reading_time',
                    'filename')
    list_filter = ('filename', 'reading_value', 'meter_serial_number', 'nmi')
    ordering = ['reading_time']
    search_fields = ('meter_serial_number', 'nmi')
    list_per_page = 10


admin.site.register(MeterReading, MeterReadingAdmin)
