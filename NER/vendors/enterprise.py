from NER.vendors.vendor import Vendor, ChargeType
import NER.util.ner_configs
from NER.util.ner_configs import southwest_config
import logging
import re
from decimal import Decimal as D
from datetime import date
import dateparser
import datetime


class Enterprise(Vendor):
    @staticmethod
    def matches_vendor(text):
        return text.find("Enterprise") >= 0

    @staticmethod
    def get_vendor_name():
        return "Enterprise Car Rental"

    @staticmethod
    def charge_type():
        return ChargeType.CAR_RENTAL

    def get_expense_charge(self):
        return self._cost

    def get_expense_date(self):
        return self._date

    def parsed_correctly(self):
        return None not in [self._date, self._cost]

    def __init__(self, ocr_text):
        self.logger = logging.getLogger(__name__)
        self._date = None
        self._cost = None
        self._ocr_text = ocr_text

        charge_pattern = re.compile(r'\(\$([0-9]{2,3}\.[0-9]{2})\)')
        found_list = charge_pattern.findall(ocr_text)
        if len(found_list) == 1:
            self.logger.debug("Found a price: '%s'", str(found_list))
            self._cost = float(found_list[0])
        else:
            charge_patter2 = re.compile('total.*?([0-9]{2,3}\.[0-9]{2}).*')
            charge_match = charge_patter2.search(ocr_text)
            if charge_match:
                self._cost = float(charge_match.groups(1)[0])

        date_pattern = re.compile(".*Pickup.*?,(.*?)([0-9]{1,2}).*([0-9]{4}).*PM.*Return.*", re.DOTALL)
        try:
            date_found = date_pattern.search(ocr_text)
            if date_found:
                self.logger.debug("Date found: '%s'", str(" ".join(date_found.groups())))
                self._date = dateparser.parse(" ".join(date_found.groups())).date()
            else:
                date_found2 = re.compile(r'Rental For (.*) ([0-9]{1,2}).*([0-9]{4})')
                date_match = date_found2.search(ocr_text)
                if date_match:
                    self._date = dateparser.parse(" ".join(date_match.groups())).date()

                self.logger.debug("Date not found.")
        except:
            self.logger.exception("An error occured while searching for the date")

        if not self.parsed_correctly():
            self.logger.warning("Enterprise did not parse a file correctly")
            self.logger.debug(repr(self._ocr_text))
