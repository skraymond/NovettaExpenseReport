import unittest
from NER.vendors.southwest import Southwest
from NER.vendors.vendor import ChargeType
from datetime import date


class MyTestCase(unittest.TestCase):
    test_string = "test string"
    good_sw_text = "9/16/2019 Southwest Airlines | My Account, Trips, Past, Details\nPast " \
                   "Flight\n\nWashington (Reagan National), DC fo San Antonio, TX\nConfirmation # " \
                   "NKQ6UG\n\nPASSENGER POINTS EARNED FARE TOTAL\n\nFirstname Lastname + 1,708PTs $476.00\n\nRR " \
                   "444112\n\nROUTING DATE FARE TYPE FARE\n\nDCA to SAT 8/26/2019 Wanna Get Away " \
                   "$142.33\nGov't taxes and fees $33 67\n\nTotal $176.00\n\nTotal points earned + 1," \
                   "708PTS\n\nhttps://www.southwest.com/myaccount/trips/past/details " \
                   "?confirmationNumber=NKQ6UG "

    def helper_function(self, ocr_text, correct_cost, correct_date):
        sw = Southwest(ocr_text)
        self.assertTrue(Southwest.matches_vendor(ocr_text))
        self.assertEqual(ChargeType.AIRPLANE, sw.get_expense_charges()[0].charge_type)
        self.assertEqual(1, len(sw.get_expense_charges()))
        self.assertEqual(correct_cost, sw.get_expense_charges()[0].charge_amount)
        self.assertEqual(correct_date, sw.get_expense_charges()[0].charge_date)
        self.assertEqual(correct_date, sw.get_expense_dates()[0])

    def test_southwest_match_vendor(self):
        self.assertTrue(Southwest.matches_vendor(self.good_sw_text))
        self.assertFalse(Southwest.matches_vendor(self.test_string))

    def test_southwest_charge_type(self):
        self.assertEqual(Southwest.charge_type(), ChargeType.AIRPLANE)

    def test_southwest_price(self):
        self.helper_function(self.good_sw_text, 176.00, date.fromisoformat("2019-08-26"))

    def test_southwest_str(self):
        self.assertEqual("Vendor named Southwest of type AIRPLANE cost 176.00 on date 2019-08-26",
                         str(Southwest(self.good_sw_text)))

    def test_southwest_parse_error_01(self):
        parsed_text = "3/15/2019 Southwest Airlines | My Account, Trips, Past, Details\nPast Flight\n\nWashington (" \
                      "Reagan National), DC fo San Antonio, TX\nConfirmation # JYC6HX\n\nPASSENGER POINTS EARNED FARE " \
                      "TOTAL\n\nFirstname Lastname + 12,584PTs $586.68\n\nRR 444112\n\nROUTING DATE FARE TYPE " \
                      "FARE\n\nDCA to SAT 2/11/2019 Business Select $524.35\n\nGov't taxes and fees $62.33\n\nTotal " \
                      "°586.68\n\nTotal points earned + 12, " \
                      "584PTS\n\nhttps://www.southwest.com/myaccount/trips/past/details ?confirmationNumber=JY C6HX "
        self.helper_function(parsed_text, 586.68, date.fromisoformat("2019-02-11"))

    def test_southwest_parse_error_02(self):
        parsed_text = "1/22/2019 Southwest Airlines | My Account, Trips, Past, Details\nPast Flight\n\nSan Antonio, " \
                      "TX to Washington (Reagan National), DC\nConfirmation # JWZM4P\n\nPASSENGER POINTS EARNED FARE " \
                      "TOTAL\n\nFirstname Lastname + 3,170PTS $310.90\n\nRR 444112\n\nROUTING DATE FARE TYPE " \
                      "FARE\n\nSAT toDCA 12/06/2018 Wanna Get Away $264.19\n\nGov't taxes and fees 546.71\n\nTotal " \
                      "°310.90\n\nTotal points earned + 3," \
                      "170PTS\n\nhttps://www.southwest.com/myaccount/trips/past/details ?confirmationNumber=JWZM4P "
        self.helper_function(parsed_text, 310.90, date.fromisoformat("2018-12-06"))

    def test_southwest_parse_error_03(self):
        parsed_text = "4/16/2019 Southwest Airlines | My Account, Trips, Past, Details\n\nPast Flight\n\nApr 7\n\nLos " \
                      "Angeles, CA to San Antonio, TX\nConfirmation # QHCO8O\n\nPASSENGER POINTS EARNED\n\nFirstname " \
                      "Lastname + 3,784?TS\n\nRR 444112\n\nROUTING DATE\n\nLAX to SAT " \
                      "4/07/2019\n\nhttps://www.southwest.com/myaccount/trips/past/details " \
                      "?confirmationNumber=QHCO8O\n\nFARE TYPE\n\nWanna Get Away\n\nGov't taxes and " \
                      "fees\n\nTotal\n\nTotal points earned\n\nFARE " \
                      "TOTAL\n\n$353.30\n\nFARE\n\n$315.35\n\n$37.95\n\n$353.30\n\n+ 3,784PTS\n\n1/1 "
        self.helper_function(parsed_text, 353.3, date.fromisoformat("2019-04-07"))

    def test_southwest_parse_error_04(self):
        parsed_text = "4/16/2019 Southwest Airlines | My Account, Trips, Past, Pricing, Details\n\nPast Flight\n\nApr " \
                      "10\n\nSan Antonio, TX to Washington (Reagan National), DC\n\nConfirmation # " \
                      "JXXYVR\n\nPASSENGER POINTS EARNED\n\nFirstname Lastname + 12,584PTs\n\nRR 444112\n\nROUTING " \
                      "DATE\n\nSAT toDCA 4/10/2019\n\nhttps://www.southwest.com/myaccount/trips/past/pricing/details " \
                      "?confirmationNumber=JXXYVR\n\nFARE TYPE\n\nBusiness Select\n\nGov't taxes and " \
                      "fees\n\nTotal\n\nTotal points earned\n\nFARE " \
                      "TOTAL\n\n$586.68\n\nFARE\n\n$524.35\n\n$62.33\n\n$586.68\n\n+ 12,584PTS\n\n1/1 "
        self.helper_function(parsed_text, 586.68, date.fromisoformat("2019-04-10"))

    def test_southwest_parse_error_05(self):
        parsed_text = "3/15/2019 Southwest Airlines | My Account, Trips, Past, Details\n\nPast Flight\n\nMar 6\n\nSan " \
                      "Antonio, TX to Washington (Reagan National), DC\n\nConfirmation # WFLJ7G\n\nPASSENGER POINTS " \
                      "EARNED\n\nFirstname Lastname + 12,584PTs\n\nRR 444112\n\nROUTING DATE\n\nSAT toDCA " \
                      "3/06/2019\n\nhttps://www.southwest.com/myaccount/trips/past/details " \
                      "?confirmationNumber=WFLJ7G\n\nFARE TYPE\n\nBusiness Select\n\nGov't taxes and " \
                      "fees\n\nTotal\n\nTotal points earned\n\nFARE " \
                      "TOTAL\n\n$586.68\n\nFARE\n\n$524.35\n\n$62.33\n\n$586.68\n\n+ 12,584PTS\n\n1/1 "
        self.helper_function(parsed_text, 586.68, date.fromisoformat("2019-03-06"))

    def test_southwest_parse_error_06(self):
        parsed_text = "9/16/2019 Southwest Airlines | My Account, Trips, Past, Details\n\nPast Flight\n\nAug " \
                      "30\n\nSan Antonio, TX to Washington (Reagan National), DC\n\nConfirmation # " \
                      "NKUKRW\n\nPASSENGER POINTS EARNED\nFirstname Lastname + 3,080°TS\n\nRR 444112\n\nROUTING " \
                      "DATE\n\nSAT toDCA 8/30/2019\n\nhttps://www.southwest.com/myaccount/trips/past/details" \
                      "?confirmationNumber=NKUKRW\n\nFARE TYPE\n\nWanna Get Away\n\nGov't taxes and " \
                      "fees\n\nTotal\n\nTotal points earned\n\nFARE " \
                      "TOTAL\n\n$299.00\n\nFARE\n\n$256.74\n\n$42.26\n\n$299.00\n\n+ 3,080PTS\n\n1/1 "
        self.helper_function(parsed_text, 299.00, date.fromisoformat("2019-08-30"))


if __name__ == '__main__':
    unittest.main()
