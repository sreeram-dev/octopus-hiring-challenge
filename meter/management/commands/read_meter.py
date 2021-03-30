# -*- coding:utf-8 -*-

import logging

from django.core.management.base import BaseCommand
from meter.processor import CSVFileProcessor


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    """
    help = 'Read a NMI file and store the readings'
    processor = CSVFileProcessor()

    def add_arguments(self, parser):
        # requires atleast one value
        parser.add_argument('files', nargs='+', type=str)

    def handle(self, *args, **options):
        files = options['files']
        for each_file in files:
            logger.info(f"Processing the following file: {each_file}")
            dtos = self.processor.process_raw_data(each_file)
            self.processor.bulk_save_data(dtos)
            logger.info(f"Finished processing the file")
