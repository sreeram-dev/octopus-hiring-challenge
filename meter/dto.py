# -*- coding:utf-8 -*-

"""Data Transfer objects for serialization and
    deserialization with various interfaces
"""

from meter.models import MeterReading


class MeterReadingDTO:
    model = MeterReading

    def __init__(self, nmi: str, meter_serial_number: str,
                 reading_value: str, read_time: 'datetime.datetime', filename: str):
        self.nmi = nmi
        self.meter_serial_number = meter_serial_number
        self.reading_value = reading_value
        self.read_time = read_time
        self.filename = filename

    def serialize_to_model(self) -> MeterReading:
        reading = MeterReading()
        reading.nmi = self.nmi
        reading.meter_serial_number = self.meter_serial_number
        reading.reading_value = self.reading_value
        reading.reading_time = self.read_time
        reading.filename = self.filename
        return reading

    @classmethod
    def deserialize(cls):
        pass

    def to_dict(self):
        return {
            'nmi': self.nmi,
            'meter_serial_number': self.meter_serial_number,
            'meter_reading_value': self.reading_value,
            'meter_read_time': self.read_time,
            'filename': self.filename
        }
