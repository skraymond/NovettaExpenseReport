import unittest
from NER.vendors.marriott import MarriottFairfax
from NER.vendors.vendor import ChargeType, Vendor, Charge
from datetime import date


class MyTestCase(unittest.TestCase):

    def helper_function(self, ocr_text, correct_charges):
        """
        @param ocr_text the original text
        @param correct_charges a list of charges
        """

        mf = MarriottFairfax(ocr_text)
        self.assertTrue(MarriottFairfax.matches_vendor(ocr_text))
        self.assertEqual(len(correct_charges), len(mf.get_expense_charges()))
        for correct_charge in correct_charges:
            charge_found = False
            for found_charge in mf.get_expense_charges():
                if correct_charge.charge_amount == found_charge.charge_amount and \
                        correct_charge.charge_type == found_charge.charge_type and \
                        correct_charge.charge_date == found_charge.charge_date:
                    charge_found = True
            self.assertTrue(charge_found, "Did not find expected charge %s" % str(correct_charge))

    def test_fairfax_marriott_dates_01(self):
        # RAYMOND_85375.pdf
        ocr_text = 'FAIRFIELD\n\nINN & SUITES®\nMatriott.\n\nS. Raymond\n\nArrive: 05Dec18\n\nDate\n\n05Dec18\n05Dec18\n05Dec18\n05Dec18\n05Dec18\n05Dec18\n06Dec18\n\nGuarantee”\n\n \n  \n\n  \n\nFairfield\n—100%—\n\n \n\n  \n\nTime: 01:17PM\n\nDescription\n\nRoom Charge\nState Occupancy Tax\n\nCity Tax\nCounty Tax\n\nValet Parking\n\nSales Tax\nVisa\n\nFairfield Inn & Suites®\n\nDepart: O6Dec18\n\nCard #: VIXXXXXXXXXXXX6779/XXXX\n\nAmount:\nFile\n\nThis card was electronically swiped on 05Dec18\n\n173.09 Auth: 02592D Signature on\n\nBalance:\n\n422 Bonham Street\nSan Antonio, TX 78205\n210.212.6262\n\nRoom: 618\nRoom Type: KING\nNumber of Guests: 1\n\nRate: $126.00 Clerk:\n\nTime: Folio Number: 85375\n\nCharges Credits\n\n126.00\n\n7.56\n\n11.34\n\n2.21\n\n24.00\n\n1.98\n173.09\n\n0.00\n\nRewards Account # XXXXX6492. Your Rewards points/miles earned on your eligible earnings will be credited to your\naccount. Check your Rewards Account Statement or your online Statement for updated activity.\n\nSee our "Privacy & Cookie Statement" on Marriott.com.\n\nOperated under license from Marriott International, Inc. or one of its affiliates.'

        mf = MarriottFairfax(ocr_text)
        self.assertEqual(date.fromisoformat("2018-12-05"), mf._arrival_date)
        self.assertEqual(date.fromisoformat("2018-12-06"), mf._departure_date)

    def test_fairfax_marriott_dates_02(self):
        ocr_text = 'Fairfield\n\nFAIRFIELD Fated\n\nINN & SUITES® ,\nGuarantee’\n\nAartriott. |\n\nFairfield Inn & Suites” 422 Bonham Street\nSan Antonio, TX 78205\n210.212.6262\n\nS. Raymond Room: 606\nRoom Type: QNQN\n\nNumber of Guests: 1\n\nRate: $126.00 Clerk:\n\nArrive: 03Dec18 Time: 05:41PM Depart: 05Dec18 Time: Folio Number: 84523\nDate Description Charges Credits\n03Dec18 Room Charge 126.00\n03Dec18 State Occupancy Tax 7.56\n03Dec18 City Tax 11.34\n03Dec18 County Tax 2.21\n03Dec18 Valet Parking 24.00\n03Dec18 Sales Tax 1.98\n04Dec18 Room Charge 126.00\n04Dec18 State Occupancy Tax 7.56\n04Dec18 City Tax 11.34\n04Dec18 County Tax 2.21\n04Dec18 Valet Parking 24.00\n04Dec18 Sales Tax 1.98\n05Dec18 Visa 346.18\n\nCard #: VIXXXXXXXXXXXX6779/XXXX\n\nAmount: 346.18 Auth: 03107D Signature on\n\nFile\nThis card was electronically swiped on 03Dec18\nBalance: 0.00\n\nRewards Account # XXXXX6492. Your Rewards points/miles earned on your eligible earnings will be credited to your\naccount. Check your Rewards Account Statement or your online Statement for updated activity.\n\nSee our "Privacy & Cookie Statement" on Marriott.com.\n\nOperated under license from Marriott International, Inc. or one of its affiliates.'
        mf = MarriottFairfax(ocr_text)
        self.assertEqual(date.fromisoformat("2018-12-03"), mf._arrival_date)
        self.assertEqual(date.fromisoformat("2018-12-05"), mf._departure_date)

    def test_fairfax_marriott_rate_01(self):
        # RAYMOND_85375.pdf
        ocr_text = 'FAIRFIELD\n\nINN & SUITES®\nMatriott.\n\nS. Raymond\n\nArrive: 05Dec18\n\nDate\n\n05Dec18\n05Dec18\n05Dec18\n05Dec18\n05Dec18\n05Dec18\n06Dec18\n\nGuarantee”\n\n \n  \n\n  \n\nFairfield\n—100%—\n\n \n\n  \n\nTime: 01:17PM\n\nDescription\n\nRoom Charge\nState Occupancy Tax\n\nCity Tax\nCounty Tax\n\nValet Parking\n\nSales Tax\nVisa\n\nFairfield Inn & Suites®\n\nDepart: O6Dec18\n\nCard #: VIXXXXXXXXXXXX6779/XXXX\n\nAmount:\nFile\n\nThis card was electronically swiped on 05Dec18\n\n173.09 Auth: 02592D Signature on\n\nBalance:\n\n422 Bonham Street\nSan Antonio, TX 78205\n210.212.6262\n\nRoom: 618\nRoom Type: KING\nNumber of Guests: 1\n\nRate: $126.00 Clerk:\n\nTime: Folio Number: 85375\n\nCharges Credits\n\n126.00\n\n7.56\n\n11.34\n\n2.21\n\n24.00\n\n1.98\n173.09\n\n0.00\n\nRewards Account # XXXXX6492. Your Rewards points/miles earned on your eligible earnings will be credited to your\naccount. Check your Rewards Account Statement or your online Statement for updated activity.\n\nSee our "Privacy & Cookie Statement" on Marriott.com.\n\nOperated under license from Marriott International, Inc. or one of its affiliates.'
        mf = MarriottFairfax(ocr_text)
        self.assertEqual(126.00, mf._rate)

    def test_fairfax_marriott_rates_02(self):
        ocr_text = 'Fairfield\n\nFAIRFIELD Fated\n\nINN & SUITES® ,\nGuarantee’\n\nAartriott. |\n\nFairfield Inn & Suites” 422 Bonham Street\nSan Antonio, TX 78205\n210.212.6262\n\nS. Raymond Room: 606\nRoom Type: QNQN\n\nNumber of Guests: 1\n\nRate: $126.00 Clerk:\n\nArrive: 03Dec18 Time: 05:41PM Depart: 05Dec18 Time: Folio Number: 84523\nDate Description Charges Credits\n03Dec18 Room Charge 126.00\n03Dec18 State Occupancy Tax 7.56\n03Dec18 City Tax 11.34\n03Dec18 County Tax 2.21\n03Dec18 Valet Parking 24.00\n03Dec18 Sales Tax 1.98\n04Dec18 Room Charge 126.00\n04Dec18 State Occupancy Tax 7.56\n04Dec18 City Tax 11.34\n04Dec18 County Tax 2.21\n04Dec18 Valet Parking 24.00\n04Dec18 Sales Tax 1.98\n05Dec18 Visa 346.18\n\nCard #: VIXXXXXXXXXXXX6779/XXXX\n\nAmount: 346.18 Auth: 03107D Signature on\n\nFile\nThis card was electronically swiped on 03Dec18\nBalance: 0.00\n\nRewards Account # XXXXX6492. Your Rewards points/miles earned on your eligible earnings will be credited to your\naccount. Check your Rewards Account Statement or your online Statement for updated activity.\n\nSee our "Privacy & Cookie Statement" on Marriott.com.\n\nOperated under license from Marriott International, Inc. or one of its affiliates.'
        mf = MarriottFairfax(ocr_text)
        self.assertEqual(126.00, mf._rate)

    def test_fairfax_marriott_01(self):
        # RAYMOND_85375.pdf
        ocr_text = 'FAIRFIELD\n\nINN & SUITES®\nMatriott.\n\nS. Raymond\n\nArrive: 05Dec18\n\nDate\n\n05Dec18\n05Dec18\n05Dec18\n05Dec18\n05Dec18\n05Dec18\n06Dec18\n\nGuarantee”\n\n \n  \n\n  \n\nFairfield\n—100%—\n\n \n\n  \n\nTime: 01:17PM\n\nDescription\n\nRoom Charge\nState Occupancy Tax\n\nCity Tax\nCounty Tax\n\nValet Parking\n\nSales Tax\nVisa\n\nFairfield Inn & Suites®\n\nDepart: O6Dec18\n\nCard #: VIXXXXXXXXXXXX6779/XXXX\n\nAmount:\nFile\n\nThis card was electronically swiped on 05Dec18\n\n173.09 Auth: 02592D Signature on\n\nBalance:\n\n422 Bonham Street\nSan Antonio, TX 78205\n210.212.6262\n\nRoom: 618\nRoom Type: KING\nNumber of Guests: 1\n\nRate: $126.00 Clerk:\n\nTime: Folio Number: 85375\n\nCharges Credits\n\n126.00\n\n7.56\n\n11.34\n\n2.21\n\n24.00\n\n1.98\n173.09\n\n0.00\n\nRewards Account # XXXXX6492. Your Rewards points/miles earned on your eligible earnings will be credited to your\naccount. Check your Rewards Account Statement or your online Statement for updated activity.\n\nSee our "Privacy & Cookie Statement" on Marriott.com.\n\nOperated under license from Marriott International, Inc. or one of its affiliates.'

        self.helper_function(ocr_text, [Charge(126.00, ChargeType.HOTEL, date.fromisoformat("2018-12-05")),
                                        Charge(7.56, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-05")),
                                        Charge(11.34, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-05")),
                                        Charge(2.21, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-05")),
                                        Charge(1.98, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-05")),
                                        Charge(24.00, ChargeType.PARKING, date.fromisoformat("2018-12-05"))
                                        ])

    def test_fairfax_marriott_02(self):
        # RAYMOND_84523.pdf
        ocr_text = 'Fairfield\n\nFAIRFIELD Fated\n\nINN & SUITES® ,\nGuarantee’\n\nAartriott. |\n\nFairfield Inn & Suites” 422 Bonham Street\nSan Antonio, TX 78205\n210.212.6262\n\nS. Raymond Room: 606\nRoom Type: QNQN\n\nNumber of Guests: 1\n\nRate: $126.00 Clerk:\n\nArrive: 03Dec18 Time: 05:41PM Depart: 05Dec18 Time: Folio Number: 84523\nDate Description Charges Credits\n03Dec18 Room Charge 126.00\n03Dec18 State Occupancy Tax 7.56\n03Dec18 City Tax 11.34\n03Dec18 County Tax 2.21\n03Dec18 Valet Parking 24.00\n03Dec18 Sales Tax 1.98\n04Dec18 Room Charge 126.00\n04Dec18 State Occupancy Tax 7.56\n04Dec18 City Tax 11.34\n04Dec18 County Tax 2.21\n04Dec18 Valet Parking 24.00\n04Dec18 Sales Tax 1.98\n05Dec18 Visa 346.18\n\nCard #: VIXXXXXXXXXXXX6779/XXXX\n\nAmount: 346.18 Auth: 03107D Signature on\n\nFile\nThis card was electronically swiped on 03Dec18\nBalance: 0.00\n\nRewards Account # XXXXX6492. Your Rewards points/miles earned on your eligible earnings will be credited to your\naccount. Check your Rewards Account Statement or your online Statement for updated activity.\n\nSee our "Privacy & Cookie Statement" on Marriott.com.\n\nOperated under license from Marriott International, Inc. or one of its affiliates.'
        self.helper_function(ocr_text, [Charge(126.00, ChargeType.HOTEL, date.fromisoformat("2018-12-03")),
                                        Charge(7.56, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-03")),
                                        Charge(11.34, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-03")),
                                        Charge(2.21, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-03")),
                                        Charge(1.98, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-03")),
                                        Charge(24.00, ChargeType.PARKING, date.fromisoformat("2018-12-03")),
                                        Charge(126.00, ChargeType.HOTEL, date.fromisoformat("2018-12-04")),
                                        Charge(7.56, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-04")),
                                        Charge(11.34, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-04")),
                                        Charge(2.21, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-04")),
                                        Charge(1.98, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-04")),
                                        Charge(24.00, ChargeType.PARKING, date.fromisoformat("2018-12-04"))])

    def test_fairfax_marriott_03(self):
        # RAYMOND_84523.pdf
        ocr_text = 'Fairfield\n\nFAIRFIELD Fated\n\nINN & SUITES® ,\nGuarantee’\n\nAartriott. |\n\nFairfield Inn & ' \
                   'Suites” 422 Bonham Street\nSan Antonio, TX 78205\n210.212.6262\n\nS. Raymond Room: 606\nRoom ' \
                   'Type: QNQN\n\nNumber of Guests: 1\n\nRate: $126.00 Clerk:\n\nArrive: 03Dec18 Time: 05:41PM ' \
                   'Depart: 05Dec18 Time: Folio Number: 84523\nDate Description Charges Credits\nxxx Room Charge ' \
                   '126.00\nxxx State Occupancy Tax 7.56\nxxx City Tax 11.34\nxxx County Tax ' \
                   '2.21\nxxxx Valet Parking 24.00\nxxx Sales Tax 1.98\nxxx Room Charge 126.00\nxxx ' \
                   'State Occupancy Tax 7.56\nxxx City Tax 11.34\nxxx County Tax 2.21\nxxx Valet Parking ' \
                   '24.00\nxxx Sales Tax 1.98\nxxx Visa 346.18\n\nCard #: VIXXXXXXXXXXXX6779/XXXX\n\nAmount: ' \
                   '346.18 Auth: 03107D Signature on\n\nFile\nThis card was electronically swiped on ' \
                   'xxxx\nBalance: 0.00\n\nRewards Account # XXXXX6492. Your Rewards points/miles earned on your ' \
                   'eligible earnings will be credited to your\naccount. Check your Rewards Account Statement or your ' \
                   'online Statement for updated activity.\n\nSee our "Privacy & Cookie Statement" on ' \
                   'Marriott.com.\n\nOperated under license from Marriott International, Inc. or one of its ' \
                   'affiliates. '
        self.helper_function(ocr_text, [Charge(126.00, ChargeType.HOTEL, date.fromisoformat("2018-12-03")),
                                        Charge(7.56, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-03")),
                                        Charge(11.34, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-03")),
                                        Charge(2.21, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-03")),
                                        Charge(1.98, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-03")),
                                        Charge(24.00, ChargeType.PARKING, date.fromisoformat("2018-12-03")),
                                        Charge(126.00, ChargeType.HOTEL, date.fromisoformat("2018-12-04")),
                                        Charge(7.56, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-04")),
                                        Charge(11.34, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-04")),
                                        Charge(2.21, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-04")),
                                        Charge(1.98, ChargeType.LODGING_TAX, date.fromisoformat("2018-12-04")),
                                        Charge(24.00, ChargeType.PARKING, date.fromisoformat("2018-12-04"))])


if __name__ == '__main__':
    unittest.main()
