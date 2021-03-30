# -*-coding:utf-8-*-

from typing import List
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from octopus.settings import BASE_DIR
from meter.models import MeterReading


class CommandTestCase(TestCase):

    def call_command(self, *args, **kwargs):
        out = StringIO()
        err = StringIO()
        try:
            call_command(
                "read_meter",
                *args,
                stdout=out,
                stderr=err,
                **kwargs
            )
        except Exception as e:
            err.write(str(e))
        return out.getvalue(), err.getvalue()

    def test_no_file(self):
        out, err = self.call_command()
        self.assertFalse(out)
        self.assertTrue(" the following arguments are required: files" in err)

    def test_valid_file(self):
        path = BASE_DIR.joinpath("tests/integration/testdata.csv")
        self.call_command(path)
        readings = MeterReading.objects.count()
        self.assertEqual(10, readings)

    def test_valid_multiple_files(self):
        path = BASE_DIR.joinpath("tests/integration/testdata.csv")
        self.call_command(path, path)
        readings = MeterReading.objects.count()
        self.assertEqual(20, readings)
