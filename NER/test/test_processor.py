import unittest
from NER.novetta_expense_report_processor import NERProcessor
import os


class MyTestCase(unittest.TestCase):
    def test_southwest_pdf(self):
        files = [os.path.join(os.path.abspath('./'), 'test_airline_files', 'southwest.pdf')]

        ner = NERProcessor()
        ner.process(files=files)


#    def test_southwest_error_pdf(self):
#        files = [os.path.join(r'C:\Users\skray\PycharmProjects\NovettaExpenseReport\NER\test\test_files', 'Southwest Airlines _ My Account, Trips, Past, Details(1).pdf')]
#
#        ner = NERProcessor()
#        ner.process(files=files)


if __name__ == '__main__':
    unittest.main()
