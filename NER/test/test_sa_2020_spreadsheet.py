import NER.util.ner_configs
from NER.spreadsheet.spreadsheet import SanAntonio2020SpreadSheet
from NER.vendors.vendor import Vendor, ChargeType
import unittest
import datetime
import os


class TestVendor(Vendor):
    ct = None

    @staticmethod
    def matches_vendor(text):
        return True

    @staticmethod
    def get_vendor_name():
        return "Test Vendor"

    @staticmethod
    def charge_type():
        return TestVendor.ct

    def __init__(self, charge, date):
        self.charge = charge
        self.date = date

    def get_expense_charge(self):
        return self.charge

    def get_expense_date(self):
        return self.date

    def parsed_correctly(self):
        return True


class MyTestCase(unittest.TestCase):

    def test_create_spreadsheet(self):
        output_filename = "%s_test.xls" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        spreadsheet = SanAntonio2020SpreadSheet(output_filename=output_filename)

        spreadsheet.create_and_open_output_file()
        self.assertTrue(os.path.exists(output_filename))

        spreadsheet.process_static_information()

        # TODO: Validate the information placed in the cells
        os.remove(output_filename)

    def test_vendor_dates(self):
        output_filename = "%s_test.xls" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        spreadsheet = SanAntonio2020SpreadSheet(output_filename=output_filename)
        spreadsheet.add_vendor(TestVendor(float(99), datetime.datetime.fromisoformat('2020-04-15')))
        spreadsheet.add_vendor(TestVendor(float(99), datetime.datetime.fromisoformat('2020-04-14')))
        spreadsheet.add_vendor(TestVendor(float(99), datetime.datetime.fromisoformat('2020-04-12')))
        spreadsheet.add_vendor(TestVendor(float(99), datetime.datetime.fromisoformat('2020-04-10')))

        self.assertEqual(4, len(spreadsheet._vendors))
        self.assertEqual(datetime.datetime.fromisoformat('2020-04-15'), spreadsheet._to_date)
        self.assertEqual(datetime.datetime.fromisoformat('2020-04-10'), spreadsheet._from_date)

    def test_write_vendor_dates(self):
        output_filename = "%s_test.xls" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        spreadsheet = SanAntonio2020SpreadSheet(output_filename=output_filename)
        spreadsheet.add_vendor(TestVendor(float(99), datetime.datetime.fromisoformat('2020-04-15')))
        spreadsheet.add_vendor(TestVendor(float(99), datetime.datetime.fromisoformat('2020-04-14')))
        spreadsheet.add_vendor(TestVendor(float(99), datetime.datetime.fromisoformat('2020-04-12')))
        spreadsheet.add_vendor(TestVendor(float(99), datetime.datetime.fromisoformat('2020-04-10')))

        spreadsheet.create_and_open_output_file()
        spreadsheet.process_date_information()
        # TODO: Validate the information placed in the cells
        os.remove(output_filename)

    def test_write_airline_vendors(self):
        TestVendor.ct = ChargeType.AIRPLANE
        output_filename = "%s_test.xls" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        spreadsheet = SanAntonio2020SpreadSheet(output_filename=output_filename)
        spreadsheet.add_vendor(TestVendor(float(99.15), datetime.datetime.fromisoformat('2020-04-15')))
        spreadsheet.add_vendor(TestVendor(float(99.10), datetime.datetime.fromisoformat('2020-04-10')))

        self.assertEqual(TestVendor.charge_type(), ChargeType.AIRPLANE)

        spreadsheet.create_and_open_output_file()
        spreadsheet.process_vendors()
        # TODO: Validate the information placed in the cells
        os.remove(output_filename)


if __name__ == '__main__':
    unittest.main()
