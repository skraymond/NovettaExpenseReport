from NER.vendors.vendor import Vendor, ChargeType, Charge
import NER.util.ner_configs
from NER.util.ner_configs import southwest_config
import logging
import re
from decimal import Decimal as D
from datetime import date
import dateparser
import datetime


class Uber(Vendor):
    @staticmethod
    def matches_vendor(text):
        return text.find('Uber') >= 0

    @staticmethod
    def get_vendor_name():
        return "Uber"

    @staticmethod
    def charge_type():
        return ChargeType.UBER

    def get_expense_charges(self):
        return [Charge(self._cost, ChargeType.UBER, self._date)]

    def get_expense_dates(self):
        return [self._date]

    def parsed_correctly(self):
        return None not in [self._date, self._cost]

    def __init__(self, ocr_text):
        self._cost = None
        self._date = None
        self.logger = logging.getLogger(__name__)
        self._ocr_text = ocr_text

        charge_pattern = re.compile('Total.*\$([0-9]{1,2}\.[0-9]{2})')
        charge_match = charge_pattern.search(ocr_text)
        if charge_match:
            self.logger.debug("Found cost: %s", str(charge_match.groups()))
            self._cost = float(charge_match.groups(1)[0])
        else:
            charge_pattern = re.compile(r'Trip fare ([0-9]{1,2}.[0-9]{2})')
            charge_match = charge_pattern.search(ocr_text)
            if charge_match:
                self.logger.debug("Found cost (alt): %s", str(charge_match.groups()))
                self._cost = float(charge_match.groups(1)[0])

        date_pattern = re.compile(r'.*?,(.{3,5})(\d{2}), (\d{4}) at.*')
        date_found = date_pattern.search(ocr_text)
        if date_found:
            self.logger.debug("Date found: '%s'", str(" ".join(date_found.groups())))
            self._date = dateparser.parse(" ".join(date_found.groups())).date()
        else:
            date_pattern = re.compile(r'\w{3}, (\w{3}) (\d{2}), (\d{4}).*')
            date_found = date_pattern.search(ocr_text)
            if date_found:
                self.logger.debug("Date found: '%s'", str(" ".join(date_found.groups())))
                self._date = dateparser.parse(" ".join(date_found.groups())).date()

        if not self.parsed_correctly():
            self.logger.warning("Uber did not parse a file correctly")
            self.logger.debug(repr(self._ocr_text))
