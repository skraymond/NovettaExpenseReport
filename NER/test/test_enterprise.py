import unittest

import unittest
from NER.vendors.enterprise import Enterprise
from NER.vendors.vendor import ChargeType
from datetime import date

class MyTestCase(unittest.TestCase):

    def test_enterprise_match_vendor(self):
        ocr_text = '-©Snterprise\n\nRenter Information\n\nRenter Name\nSPENCER RAYMOND\n\nRenter Address\nWASHINGTON, ' \
                   'DC 20002\nUSA\n\nContract\nNOVETTA SOLUTIONS\n\nVehicle Information\n\n4DR SEDAN\nLicense #: ' \
                   'MGJ5551\nState/Province: TX\nUnit #: 7SQHCM\nVehicle #: KY373543\n\nVehicle Class ' \
                   'Driven\nIntermediate Car 2 or 4-Door/\n\nAutomatic/Air\n\nVehicle Class Charged\nIntermediate Car ' \
                   '2 or 4-Door/\n\nAutomatic/Air\n\nOdometer Mileage/Kilometers\n\nStarting: 2,344 Ending: 2,' \
                   '499\n\nTotal: 155\n\nThank you for renting\nwith Enterprise Rent-A-\nCar\n\nWe appreciate your ' \
                   'business!\n\nThis email was automatically generated\nfrom an unattended mailbox, so please\ndo ' \
                   'not reply to this e-mail.\n\nIf you have any questions about your\n\nrental, please view our ' \
                   'Frequently\n\nTrip Information\n\nPickup\n\nMonday, August 26, 2019 5:06 PM\nStart ' \
                   'Charges\n\nMonday, August 26, 2019 5:09 PM\n\nSAN ANTONIO INTL ARPT (SAT)\n9559 AIRPORT ' \
                   'BLVD\n\nSAN ANTONIO, TX 78216\n\nUSA\n\nRental Agreement # 347105065\nInvoice # ' \
                   '90118871885\n\nReturn\nFriday, August 30, 2019 8:36 AM\nSAN ANTONIO INTL ARPT (SAT)\n9559 AIRPORT ' \
                   'BLVD\nSAN ANTONIO, TX 78216\nUSA\n\nBill-To: NOVETTA SOLUTIONS\n\nSubtotal\n\nRenter ' \
                   'Charges\n\nRental Rate\n\nTaxes and Fees\n\nTime & Distance 4 Day at $33.45 / Day\n\nTx Motor Veh ' \
                   'Rental Tax (10.00%)\n\n$133.80\n\n$18.40\n\nFacility Management Fee 0.80/day ($0.80 ' \
                   '/\n\nDay)\n\nConcession Fee Recovery 11.11 Pct (11.11%)\nBexar Sports Venue Tax 5 Pct (' \
                   '5.00%)\nVif Rec 2.29/day ($2.29 / Day)\n\n$3.20\n$15.88\n$9.20\n$9.16\n\nConsolidated Facility ' \
                   'Chg 5.50/day ($5.50 /\n\nDay)\n\nTotal\n\n(Subject to audit)\n\nAmount charged on August 30, ' \
                   '2019 to VISA (6779)\n\nAmount Due\n\n$22.00\n\n$211.64\n\n($211.64)\n$0.00Thank you for ' \
                   'renting\nwith Enterprise Rent-A-\nCar\n\nAsked Questions or send usa secured\n\nmessage by ' \
                   'visiting our Support Center '
        self.assertTrue(Enterprise.matches_vendor(ocr_text))
        self.assertFalse(Enterprise.matches_vendor("Test string"))

    def test_enterprise_charge_type(self):
        self.assertEqual(Enterprise.charge_type(), ChargeType.CAR_RENTAL)

    def helper_function(self, ocr_text, correct_cost, correct_date):
        ep = Enterprise(ocr_text)
        self.assertTrue(Enterprise.matches_vendor(ocr_text))
        self.assertEqual(correct_cost, ep.get_expense_charge())
        self.assertEqual(correct_date, ep.get_expense_date())

    def test_enterprise_parse_test_01(self):
        ocr_text = '-©Snterprise\n\nRenter Information\n\nRenter Name\nSPENCER RAYMOND\n\nRenter Address\nWASHINGTON, ' \
                   'DC 20002\nUSA\n\nContract\nNOVETTA SOLUTIONS\n\nVehicle Information\n\n4DR SEDAN\nLicense #: ' \
                   'MGJ5551\nState/Province: TX\nUnit #: 7SQHCM\nVehicle #: KY373543\n\nVehicle Class ' \
                   'Driven\nIntermediate Car 2 or 4-Door/\n\nAutomatic/Air\n\nVehicle Class Charged\nIntermediate Car ' \
                   '2 or 4-Door/\n\nAutomatic/Air\n\nOdometer Mileage/Kilometers\n\nStarting: 2,344 Ending: 2,' \
                   '499\n\nTotal: 155\n\nThank you for renting\nwith Enterprise Rent-A-\nCar\n\nWe appreciate your ' \
                   'business!\n\nThis email was automatically generated\nfrom an unattended mailbox, so please\ndo ' \
                   'not reply to this e-mail.\n\nIf you have any questions about your\n\nrental, please view our ' \
                   'Frequently\n\nTrip Information\n\nPickup\n\nMonday, August 26, 2019 5:06 PM\nStart ' \
                   'Charges\n\nMonday, August 26, 2019 5:09 PM\n\nSAN ANTONIO INTL ARPT (SAT)\n9559 AIRPORT ' \
                   'BLVD\n\nSAN ANTONIO, TX 78216\n\nUSA\n\nRental Agreement # 347105065\nInvoice # ' \
                   '90118871885\n\nReturn\nFriday, August 30, 2019 8:36 AM\nSAN ANTONIO INTL ARPT (SAT)\n9559 AIRPORT ' \
                   'BLVD\nSAN ANTONIO, TX 78216\nUSA\n\nBill-To: NOVETTA SOLUTIONS\n\nSubtotal\n\nRenter ' \
                   'Charges\n\nRental Rate\n\nTaxes and Fees\n\nTime & Distance 4 Day at $33.45 / Day\n\nTx Motor Veh ' \
                   'Rental Tax (10.00%)\n\n$133.80\n\n$18.40\n\nFacility Management Fee 0.80/day ($0.80 ' \
                   '/\n\nDay)\n\nConcession Fee Recovery 11.11 Pct (11.11%)\nBexar Sports Venue Tax 5 Pct (' \
                   '5.00%)\nVif Rec 2.29/day ($2.29 / Day)\n\n$3.20\n$15.88\n$9.20\n$9.16\n\nConsolidated Facility ' \
                   'Chg 5.50/day ($5.50 /\n\nDay)\n\nTotal\n\n(Subject to audit)\n\nAmount charged on August 30, ' \
                   '2019 to VISA (6779)\n\nAmount Due\n\n$22.00\n\n$211.64\n\n($211.64)\n$0.00Thank you for ' \
                   'renting\nwith Enterprise Rent-A-\nCar\n\nAsked Questions or send usa secured\n\nmessage by ' \
                   'visiting our Support Center '
        self.helper_function(ocr_text, 211.64, date.fromisoformat("2019-08-26"))

    def test_enterprise_parse_test_02(self):
        # 0410 - Enterprise.pdf
        ocr_text = '-©nterprise\n\nRenter Information\n\nRenter Name\nSPENCER RAYMOND\n\nRenter Address\nWASHINGTON, DC 20002\nUSA\n\nContract\nENTERPRISE PLUS\n\nVehicle Information\n\nTUCSON SEL AWD\nLicense #: GVV192\nState/Province: IA\nUnit #: 7QN2FX\nVehicle #: JU708244\n\nVehicle Class Driven\nIntermediate SUV 4-Door/Automatic/Air\n\nVehicle Class Charged\nIntermediate SUV 4-Door/Automatic/Air\n\nOdometer Mileage/Kilometers\n\nStarting: 25,354 Ending: 25,425\n\nTotal: 71\n\nThank you for renting with\nEnterprise Rent-A-Car\n\nWe appreciate your business!\n\nThis email was automatically generated\nfrom an unattended mailbox, so please do\nnot reply to this e-mail.\n\nIf you have any questions about your\nrental, please view our Frequently Asked\n\nQuestions or send us a secured message\n\nby visiting our Support Center\n\nTrip Information\n\nPickup\n\nSunday, April 7, 2019 1:16 PM\nStart Charges\n\nSunday, April 7, 2019 1:21 PM\n\nSAN ANTONIO INTL ARPT (SAT)\n9559 AIRPORT BLVD\n\nSAN ANTONIO, TX 78216\n\nUSA\n\nRental Charges\n\nRental Rate\nAdd-Ons Discount (5.00%)\nMileage Unlimited Mileage\n\nTaxes and Fees\n\nRental Agreement # 345252783\nInvoice # 90113781807\n\nReturn\n\nWednesday, April 10, 2019\nSAN ANTONIO INTL ARPT (SAT)\n9559 AIRPORT BLVD\nSAN ANTONIO, TX 78216\nUSA\n\nTime & Distance 3 Day at $44.99 / Day\n\nConcession Fee Recovery 11.11 Pct (11.11%)\n\nConsolidated Facility Chg 5.50/day ($5.50 / Day)\nBexar Sports Venue Tax 5 Pct (5.00%)\n\nVIf Rec 1.99/day ($1.99 / Day)\n\nFacility Management Fee 0.80/day ($0.80 / Day)\nTx Motor VehRental Tax (10.00%)\n\nTotal\n\n(Subject to audit)\n\nAmount charged on April 10, 2019 to VISA (9657)\n\nAmount Due\n\n9:45 AM\n\n$134.97\n-$6.75\nIncluded\n\n$14.91\n$16.50\n$8.40\n$5.97\n$2.40\n$16.80\n\n$193.20\n\n($193.20)\n$0.00'
        self.helper_function(ocr_text, 193.20, date.fromisoformat("2019-04-07"))

    def test_enterprise_parse_test_03(self):
        # 20181206 Enterprise.pdf
        ocr_text = '1/22/2019\n\nRental For Dec 03, 2018\nRental Agreement #: 343837208\n\nEnterprise Plus Login | Enterprise Rent-A-Car\n\nQ Customer Service: 855-287-4216\n\nPICK-UP RETURN\nSan Antonio International Airport 03 Dec 2018 = San Antonio International Airport 06 Dec 2018\nSan Antonio, TX 5:13 PM San Antonio, TX 2:20 PM\n\n+1 210-640-4966\n\nFINAL TOTAL (USD)\n\n$233\n\nRental Charges\n\n \n\n \n\n \n\n \n\n \n\nVEHICLE\nTIME & DISTANCE $ 55.07 / day $ 165.21\nEXTRAS\n\nREFUELING CHARGE $ 3.33 / gallon $ 3.33\nMISCELLANEOUS\n\nDISCOUNT $ -8.26\nTAXES & FEES\n\nAIRPORT SURCHARGES $ 5.50 / day $ 16.50\nAIRPORT SURCHARGES $ 0.80 / day $ 2.40\nOPTIONAL SURCHARGES $ 18.46\nLEGAL MANDATED SURCHARGE $ 10.01\nVEHICLE REGISTRATION $ 1.95 / day $ 5.85\nRECOUPMENT FEE\n\nSTATE TAX $ 20.02\nTOTAL\n\ntotal (USD) $ 233.52\n\nThank you for choosing Enterprise.\n\n+1 210-640-4966\n\nRenter Details\n\n \n\nName: SPENCER RAYMOND\nMember #: M86KCTH\nAddress On File: cere A STREE***s\n\nAccount Name Enterprise Plus\n\nVehicle Details\n\n \n\nClass Driven: SCAR\n\nClass Charged: SCAR\n\n \n\nMake/Model: NISSAN SENTRA\nLicense Plate: LHS6558\nDistance\n\nOdometer Start: 2291 Miles\nOdometer End: 2326 Miles\nDistance Driven: 35 Miles\n\nEan Holdings, Llc - San Antonio International Airport - 9559 Airport Blvd, San Antonio * 78216 TX, US\n\nhttps://www.enterprise.com/en/account.html#reservation\n\n1/1'
        self.helper_function(ocr_text, 233.52, date.fromisoformat("2018-12-03"))

    # I think this is an older format of Enterprise's receipt
    # def test_enterprise_parse_test_04(self):
    #     # Enterprise Plus Account - Enterprise Rent-A-Car.pdf
    #     ocr_text = '6/7/2017\n\nRental For May 14, 2017\nRental Agreement #: 336868161\nCustomer Service: +1 855-287-4216\n\nPICK-UP\nSan Antonio International Airport\n\nSan Antonio, TX\n+1 210-348-6806\n14 May 2017\n\n11:10 PM\n\nFinal Total\n\n$ 797.36\n\nRental Charges\n\nVEHICLE\n\nTIME & DISTANCE\n$ 219.84 / week\n\nFinal Total\n\nhttps ://www.enter prise.com/en/account.html#reservation\n\nEnterprise Plus Account - Enterprise Rent-A-Car\n\nRETURN\nSan Antonio International Airport\n\nSan Antonio, TX\n+1 210-348-6806\n24 May 2017\n\n2:45 PM\n\nRenter Information\n\nName:\nSPENCER RAYMOND\n$ 219.84\nMember #:\nM86KCTH\n$ 797.36\n\nAddressOn File:\n1433 A STREET NE\nWASHINGTON, DC 20002\n\nVehicle Details\n\nClass Driven:\nECAR\n\nClass Charged:\nECAR\n\n1/26/7/2017\n\nhttps ://www.enter prise.com/en/account.html#reservation\n\nEnterprise Plus Account - Enterprise Rent-A-Car\n\nMake/Model:\nNISSAN VERSA\n\nLicense Plate:\nHTM2119\n\nDistance\n\nOdometer Start:\n\n20187 MI\n\nOdometer End:\n20678 MI\n\nDistance Driven:\n\n491 Ml\n\n2/2'
    #     self.helper_function(ocr_text, 797.36, date.fromisoformat("2017-05-14"))
    #
    # def test_enterprise_parse_test_06(self):
    #     # Enterprise Plus Login _ Enterprise Rent-A-Car.pdf
    #     ocr_text = '108036\n\nPICK-UP\n\nSan Antonio International Airport\nSan Antonio, TX\n\n+] 210-640-4966\n\n11 Jun 2019 >\n4:40 PM\n\nFINAL TOTAL (USD)\n\n$1687\n\n \n\n \n\n \n\nVEHICLE\n\nTIME & DISTANCE $ 36.27 / day ¢ 108.81\nTAXES & FEES\n\nBEXAR SPORTS VENUE TAX 5 PCT $ 7.34\nCONCESSION FEE RECOVERY 11.11 $ 12.79\nPCT\n\nCONSOLIDATED FACILITY CHG $ 5.50 / day $ 16.50\n5.50/DAY\n\nFACILITY MANAGEMENT FEE ¢ 0.80 / day $ 2.40\n0.80/DAY\n\nVLF REC 2.09/DAY $ 2.09 / day $ 6.27\nTX MOTOR VEH RENTAL TAX $ 14.68\nTOTAL\n\ntotal (USD) $ 168.79\n\nThank you for choosing Enterprise.\n\nRETURN\n\nSan Antonio International Airport\nSan Antonio, TX\n\n+] 210-640-4966\n\nQO Customer Service: 855-287-4216\n\n \n\n14 Jun 2019\n\n3:10 PM\nRENTER DETAILS\nName: SPENCER RAYMOND\nMember #: M86KCTH\nAddress On File: core A STREE**se\n\nAccount Name Novetta - Cpg\n\n \n\n \n\nVEHICLE DETAILS\nClass Driven: FCAR\n\nClass Charged: FCAR\nMake/Model: TOYOTA CAMRY\nLicense Plate: FP46706\nDISTANCE\n\nOdometer Start: 16109 Miles\nOdometer End: 16185 Miles\nDistanceDriven: 76 MilesEan Holdings, Llc * San Antonio International Airport » 9559 Airport Blvd, San Antonio * 78216 IX,\nUS'
    #     self.helper_function(ocr_text, 168.79, date.fromisoformat("2019-06-14"))

if __name__ == '__main__':
    unittest.main()
