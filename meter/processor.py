# -*- coding:utf-8 -*-

import datetime
import logging

from os.path import basename
from itertools import islice
from pathlib import Path
from typing import List

from django.utils.timezone import make_aware

from meter.dto import MeterReadingDTO
from meter.models import MeterReading


logger = logging.getLogger(__name__)


class IProcessorInterface:

    def process_raw_data(self, filepath: str) -> List[MeterReadingDTO]:
        """Process raw data from a file or a streaud
        :param: filepath: path to the file that has to be processed
        """
        raise NotImplementedError

    def bulk_save_data(self):
        raise NotImplementedError


class CSVFileProcessor(IProcessorInterface):

    def process_raw_data(self, filepath: str) -> List[MeterReadingDTO]:
        data = []
        path = Path(filepath)
        if not path.exists():
            raise ValueError(f"File with path does not exist: {filepath}")

        with path.open('r') as fp:
            # skip header file
            lines = fp.readlines()[1:]
            for line in lines:
                try:
                    meter_dto = self.process_each_line(line, ",", filepath)
                    data.append(meter_dto)
                except ValueError:
                    # incomplete data just ignore and process the next fields
                    pass
        logger.info(f"Fetched {len(data)} objects from the file: {basename(filepath)}")
        return data

    def process_each_line(self, record: str, delimiter: str, filepath: str) -> MeterReadingDTO:
        """Process the line and return the DTO Object
        NMI -> 2nd Column
        Meter Serial Values ->7th Column
        Meter Reading Value (CurrentRegisterRead) -> 14th Column
        Meter Read DateTime (CurrentRegisterReadDateTime) -> 15th Column
        20040107100333 - sample input for parsing datetime
        filename -> Name of the file
        """
        columns = record.strip().split(",")
        if not (columns[1] or columns[6] or columns[13] or columns[14]):
            raise ValueError('Incomplete data present')
        reading_time = datetime.datetime.strptime(columns[14], '%Y%m%d%H%M%S')
        reading_time = make_aware(reading_time)
        dto = MeterReadingDTO(columns[1], columns[6], columns[13], reading_time, basename(filepath))
        return dto

    def bulk_save_data(self, data: List[MeterReadingDTO]):
        logger.info(f"Saving {len(data)} objects in database")

        # save 100 at a time
        offset = 0
        batch_size = 100
        while True:
            start = offset
            end = min(len(data), offset+batch_size)
            batch = list(islice(data, start, end, 1))
            objects = list(map(lambda d: d.serialize_to_model(),
                               batch))
            MeterReading.objects.bulk_create(objects, batch_size)
            offset = offset + batch_size
            if offset >= len(data):
                break

        logger.info("Meter readings saved successfully")
