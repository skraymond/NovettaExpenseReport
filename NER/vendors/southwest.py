from NER.vendors.vendor import Vendor, ChargeType, Charge
import NER.util.ner_configs
from NER.util.ner_configs import southwest_config
import logging
import re
from decimal import Decimal as D
from datetime import date


class Southwest(Vendor):

    @staticmethod
    def get_vendor_name():
        return "Southwest"

    @staticmethod
    def charge_type():
        return ChargeType.AIRPLANE

    @staticmethod
    def matches_vendor(text):
        # Most pdfs found "southwest.com", also including my SW rewards number
        return text.find("southwest.com") >= 0 or text.find(southwest_config['rapid_reward_number']) >= 0

    def __init__(self, ocr_text):
        self._date = None
        self._cost = None
        self.logger = logging.getLogger(__name__)
        self._ocr_text = ocr_text

        charge_pat = re.compile(r'Total.*?([0-9]{1,4}.[0-9]{2})$')
        date_pat = re.compile(r'[A-Z]{3} *to *[A-Z]{3} ([0-9]{1,2})/([0-9]{1,2})/([0-9]{4}).*$')
        for parse in ocr_text.split('\n'):
            charge_match = charge_pat.search(parse)
            if charge_match:
                self.logger.debug("Total found:" + parse)
                self.logger.debug("\tGroup: " + str(charge_match.groups()))
                self._cost = float(charge_match.group(1))

            date_match = date_pat.search(parse)
            if date_match:
                self.logger.debug("Date found:" + parse)
                self.logger.debug("Group: " + str(date_match.groups()))
                self.logger.debug("Date string: " + "%04d-%02d-%02d" % (int(date_match.group(3)),
                                                                        int(date_match.group(1)),
                                                                        int(date_match.group(2))))
                self._date = date.fromisoformat("%04d-%02d-%02d" % (int(date_match.group(3)),
                                                                    int(date_match.group(1)),
                                                                    int(date_match.group(2))))

        if self._cost is None:
            all_dollars = re.findall(r'\$([0-9]{2,3}\.[0-9]{2})', self._ocr_text)
            self.logger.debug("Attempting to find price through alternative mechanism, dollar amounts found: %s",
                              str(all_dollars))

            uniq_dollars = []
            for dollar in all_dollars:
                if dollar not in uniq_dollars:
                    uniq_dollars.append(dollar)
            uniq_dollars = uniq_dollars
            decimal_dollars = sorted([D(x) for x in uniq_dollars])
            if len(decimal_dollars) == 3 and decimal_dollars[0] + decimal_dollars[1] == decimal_dollars[2]:
                self._cost = float(decimal_dollars[2])

        if not self.parsed_correctly():
            self.logger.warning("Southwest did not parse a file correctly")
            self.logger.debug(repr(self._ocr_text))

    def parsed_correctly(self):
        return None not in [self._date, self._cost]

    def get_expense_dates(self):
        return [self._date]

    def get_expense_charges(self):
        return [Charge(self._cost, ChargeType.AIRPLANE, self._date)]
