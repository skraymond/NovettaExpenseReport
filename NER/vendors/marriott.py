import re
from abc import ABC
import logging
from datetime import timedelta
import NER.util.ner_configs


import dateparser

from NER.vendors.vendor import ChargeType, Vendor, Charge
from datetime import date


class Marriott(Vendor, ABC):

    @staticmethod
    def charge_type():
        pass

    def get_expense_charges(self):
        return self._charges

    def get_expense_dates(self):
        return [charge.charge_date for charge in self._charges]

    def parsed_correctly(self):
        return len(self._charges) > 0

    def __init__(self, ocr_text):
        self.ocr_text = ocr_text

        self._charges = []
        self._arrival_date = None
        self._departure_date = None
        self._rate = None


class MarriottFairfax(Marriott):
    @staticmethod
    def matches_vendor(text):
        return text.find('Fairfield Inn & Suites') > 0

    @staticmethod
    def get_vendor_name():
        return "Marriott Fairfax Hotel"

    def _set_arrival_and_departure_date(self):
        try:
            def find_arrival_departure_date(arrival_departure_text="Arrive"):
                date_pattern = re.compile(arrival_departure_text + r": (\d{2})(\w{3})(\d{2})", re.MULTILINE)

                date_match = date_pattern.search(self.ocr_text.replace('O', '0'))
                if date_match:
                    return dateparser.parse(" ".join([x for x in date_match.groups()])).date()

            self._arrival_date = find_arrival_departure_date("Arrive")
            self._departure_date = find_arrival_departure_date("Depart")
            self.logger.debug("Arrival/Departure Dates found: %s/%s", str(self._arrival_date),
                              str(self._departure_date))
        except:
            self.logger.warning("Unable to set arrival and departure date.")

    def _set_rate(self):
        try:
            rate_pattern = re.compile(r"Rate: \$(\d{1,3}\.\d{2})", re.MULTILINE)
            rate_match = rate_pattern.search(self.ocr_text)
            if rate_match:
                self._rate = float(rate_match.group(1))
        except:
            self.logger.warning("Unable to set rate")

    def __init__(self, ocr_text):
        super(MarriottFairfax, self).__init__(ocr_text)
        self.logger = logging.getLogger(__name__)

        self._set_arrival_and_departure_date()
        self._set_rate()

        # Attempt to find the dates in an easy manner
        unparsable_line = []
        easy_line_pattern = re.compile(r'(^(\d{2})(\w{3})(\d{2})(.*?)(\d{1,3}\.\d{2}$))')
        for line in re.findall(r'(^\d{2}\w{3}\d{2}.*?\d{1,3}\.\d{2}$)', ocr_text.replace('O', '0'), re.MULTILINE):
            easy_line_match = easy_line_pattern.search(line)
            self.logger.debug("Easy line parsed: %s", str(easy_line_match.groups()))

            line_date = dateparser.parse(" ".join([x for x in easy_line_match.groups()[1:4]])).date()
            self.logger.debug("Easy line parsed (date): %s", str(line_date))
            line_cost = float(easy_line_match.groups()[5])
            self.logger.debug("Easy line parsed (date): %.2f", line_cost)

            if line.find('Room Charge') > 0:
                self._charges.append(Charge(line_cost, ChargeType.HOTEL, line_date))
            elif line.find('Park') > 0:
                self._charges.append(Charge(line_cost, ChargeType.PARKING, line_date))
            elif line.find('Tax') > 0:
                self._charges.append(Charge(line_cost, ChargeType.LODGING_TAX, line_date))
            else:
                unparsable_line.append(line)
        if len(unparsable_line) > 0:
            self.logger.debug("Didn't find matches for any of the following: %s", "; ".join(unparsable_line))

        if len(self._charges) == 0:
            # This won't be precise. We're assuming anything 1%-10% of the rate is taxes, anything about the rate
            # doesn't go on our sheet, and anything else is parking
            self.logger.debug("Attempting to find charges through harder mechanism")

            phoneless_text = re.sub(r'\d{3}\.\d{3}\.\d{4}', '<phone>', ocr_text)
            all_prices_txt = re.findall(r'\d{1,3}\.\d{2}', phoneless_text)
            price_count = {}

            # First, count all the dollar amounts we've found
            for price in all_prices_txt:
                if float(price) >= self._rate:
                    self.logger.debug("Ignoring price: %s", price)
                    continue

                if price not in price_count:
                    price_count[price] = 0
                price_count[price] = price_count[price] + 1

            # Only include prices which showed up for every night
            stay_duration = (self._departure_date - self._arrival_date).days
            taxes = []
            parking = []
            for price in price_count:
                if price_count[price] != stay_duration:
                    self.logger.debug("A price (%s) was found, but not for every night of the stay (%d/%d)", price,
                                      price_count[price], stay_duration)
                    continue
                if float(price) <= 0:
                    continue
                if float(price) <= self._rate * .1:
                    taxes.append(float(price))
                else:
                    parking.append(float(price))

            for i in range(stay_duration):
                self._charges.append(Charge(self._rate, ChargeType.HOTEL, self._arrival_date + timedelta(days=i)))
                for tax in taxes:
                    self._charges.append(Charge(tax, ChargeType.LODGING_TAX, self._arrival_date + timedelta(days=i)))
                for park in parking:
                    self._charges.append(Charge(park, ChargeType.PARKING, self._arrival_date + timedelta(days=i)))


        self.logger.debug("Charges found: %s", "; \n".join([str(x) for x in self._charges]))
