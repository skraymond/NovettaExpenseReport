import unittest
from NER.vendors.uber import Uber
from NER.vendors.vendor import ChargeType
from datetime import date


class MyTestCase(unittest.TestCase):

    def test_uber_match_vendor(self):
        ocr_text = '3/15/2019 Gmail - Your Monday afternoon trip with Uber\n\nM Gmail\n\nYour Monday afternoon trip ' \
                   'with Uber\n\nUber Receipts <uber.us@uber.com>\nTo: testuser+uber@gmail.com\n\nThanks for riding,' \
                   '\n<firstname>\n\nWe hope you enjoyed your ride\nthis afternoon.\n\nTotal\n\nTrip ' \
                   'Fare\n\nSubtotal\nTolls, Surcharges, and Fees\n\nWait Time\n\nAmount Charged\n\n<firstname> <lastname> ' \
                   '<testuser@gmail.com>\n\nMon, Feb 11, 2019 at 2:56 PM\n\nTotal: $18.06\nMon, Feb 11, ' \
                   '2019\n\n$18.06\n\nYou earned 36 points on this ' \
                   'trip\n\n$11.07\n\n$11.07\n$6.83\n\n$0.16\n\nhttps://mail.google.com/mail/u/0?ik=23fb490d1a&view' \
                   '=pt&search=all&permmsgid=msg-f%3A 16252036907 70477432\n\n1/43/15/2019 Gmail - Your Monday ' \
                   'afternoon trip with Uber\n\ne666 5319 Switch $18.06\nReceipt ID # ' \
                   '51673fcd-edfa-478b-bdf5-82f482e1f9c0\n\nDownload PDF\nDownload link expires 3/13/19\n\nYou rode ' \
                   'with Yonatan\n\n4.91 Rating How was your ride?\n\nTop Driver Compliment\n\n"Excellent ' \
                   'Service"\n\nIssued by Rasier\n\nWhen you ride with Uber, your trips are insured in case of a ' \
                   'covered\naccident. Learn more.\n\n8.27 mi| 17 min\n02:39pm\n1457 Zulu St, Washington,' \
                   '\nDC\n02:56pm\n\nAviation Cir, Arlington, ' \
                   'VA\n\nhttps://mail.google.com/mail/u/0?7ik=23fb440d1a&view=pt&search=all&permmsgid=msg-f' \
                   '%3A16252036907 70477432 2/43/15/2019 Gmail - Your Monday afternoon trip with Uber\n\na\n\n4 ' \
                   'HI\n\n \n  \n\nGoogle} Map data 2019 Google\n\nInvite your friends and family.\n\nGet $5 off your ' \
                   'next ride when you refer a friend to\n\ntry Uber. Share code: 85asm\n\nREPORT LOST ITEM > CONTACT ' \
                   'SUPPORT > MY TRIPS >\nFAQ UberTechnologies\n\n1455 Market St\nForgot password San Francisco, ' \
                   'CA 94103\n\nPrivacy\n\nTerms\n\nhttps://mail.google.com/mail/u/0?7ik=23fb490d1a&view=pt&search' \
                   '=all&permmsgid=msg-f%3A16252036907 70477432 3/43/15/2019 Gmail - Your Monday afternoon trip with ' \
                   'Uber\n\nhttps://mail.google.com/mail/u/0?ik=23fb490d1a&view=pt&search=all&permmsgid=msg-f%3A ' \
                   '16252036907 70477432 4/4 '
        self.assertTrue(Uber.matches_vendor(ocr_text))
        self.assertFalse(Uber.matches_vendor("Test string"))

    def test_uber_charge_type(self):
        self.assertEqual(Uber.charge_type(), ChargeType.UBER)

    def helper_function(self, ocr_text, correct_cost, correct_date):
        ub = Uber(ocr_text)
        self.assertTrue(Uber.matches_vendor(ocr_text))
        self.assertEqual(1, len(ub.get_expense_charges()))
        self.assertEqual(ChargeType.UBER, ub.get_expense_charges()[0].charge_type)
        self.assertEqual(correct_cost, ub.get_expense_charges()[0].charge_amount)
        self.assertEqual(correct_date, ub.get_expense_charges()[0].charge_date)
        self.assertEqual(correct_date, ub.get_expense_dates()[0])

    def test_uber_parse_test_01(self):
        ocr_text = '3/15/2019 Gmail - Your Monday afternoon trip with Uber\n\nM Gmail\n\nYour Monday afternoon trip ' \
                   'with Uber\n\nUber Receipts <uber.us@uber.com>\nTo: testuser+uber@gmail.com\n\nThanks for riding,' \
                   '\n<firstname>\n\nWe hope you enjoyed your ride\nthis afternoon.\n\nTotal\n\nTrip ' \
                   'Fare\n\nSubtotal\nTolls, Surcharges, and Fees\n\nWait Time\n\nAmount Charged\n\n<firstname> <lastname> ' \
                   '<testuser@gmail.com>\n\nMon, Feb 11, 2019 at 2:56 PM\n\nTotal: $18.06\nMon, Feb 11, ' \
                   '2019\n\n$18.06\n\nYou earned 36 points on this ' \
                   'trip\n\n$11.07\n\n$11.07\n$6.83\n\n$0.16\n\nhttps://mail.google.com/mail/u/0?ik=23fb490d1a&view' \
                   '=pt&search=all&permmsgid=msg-f%3A 16252036907 70477432\n\n1/43/15/2019 Gmail - Your Monday ' \
                   'afternoon trip with Uber\n\ne666 5319 Switch $18.06\nReceipt ID # ' \
                   '51673fcd-edfa-478b-bdf5-82f482e1f9c0\n\nDownload PDF\nDownload link expires 3/13/19\n\nYou rode ' \
                   'with Yonatan\n\n4.91 Rating How was your ride?\n\nTop Driver Compliment\n\n"Excellent ' \
                   'Service"\n\nIssued by Rasier\n\nWhen you ride with Uber, your trips are insured in case of a ' \
                   'covered\naccident. Learn more.\n\n8.27 mi| 17 min\n02:39pm\n1457 Zulu St, Washington,' \
                   '\nDC\n02:56pm\n\nAviation Cir, Arlington, ' \
                   'VA\n\nhttps://mail.google.com/mail/u/0?7ik=23fb490d1a&view=pt&search=all&permmsgid=msg-f' \
                   '%3A16252036907 70477432 2/43/15/2019 Gmail - Your Monday afternoon trip with Uber\n\na\n\n4 ' \
                   'HI\n\n \n  \n\nGoogle} Map data 2019 Google\n\nInvite your friends and family.\n\nGet $5 off your ' \
                   'next ride when you refer a friend to\n\ntry Uber. Share code: 85asm\n\nREPORT LOST ITEM > CONTACT ' \
                   'SUPPORT > MY TRIPS >\nFAQ UberTechnologies\n\n1455 Market St\nForgot password San Francisco, ' \
                   'CA 94103\n\nPrivacy\n\nTerms\n\nhttps://mail.google.com/mail/u/0?7ik=23fb490d1a&view=pt&search' \
                   '=all&permmsgid=msg-f%3A16252036907 70477432 3/43/15/2019 Gmail - Your Monday afternoon trip with ' \
                   'Uber\n\nhttps://mail.google.com/mail/u/0?ik=23fb490d1a&view=pt&search=all&permmsgid=msg-f%3A ' \
                   '16252036907 70477432 4/4 '
        self.helper_function(ocr_text, 18.06, date.fromisoformat("2019-02-11"))

    def test_uber_parse_test_03(self):
        ocr_text = "Gmail - Your Sunday afternoon trip with Uber\n<firstname> <lastname> " \
                   "<testuser@gmail.com>\n\n6/7/2017\n\nM1 Gmail\nSun, May 14, 2017 at 4:05 PM\n\nYour Sunday " \
                   "afternoon trip with Uber\n\n \n \n\n1message\nUber Receipts <uber.us@uber.com>\nTo: " \
                   "testuser+uber@gmail.com\n309 Washington Fairmount\n1 St NE Benn; Heights\nSOR NE Seat " \
                   "Pleasant\nE Capitol St SE\n~ Capitol (214\n2 3 Heights\nArlington 2 |\nSee Walker M\nwld << " \
                   "CoralHills\nS Distric\n@ Height\n@) 244 2 . 18\n& 2 Suitls,.. 458\nBailey's & g & eae " \
                   ".\nCrossroads gS ye wy-Suitland-Silver Hill\nYe, © = Hillcrest\n8 Ry p Heights ©)\n¥ Map data " \
                   "©2017 Google\n\n \n\n$30.04\n\nThanks for choosing Uber,<firstname>\n\nMay 14, 2017 | uberx\n\n® " \
                   "03:42pm | 1422-1424 A St NE, Washington, DC\n\n@ 04:04pm | 1 Aviation Cir, Arlington, " \
                   "VA\n\nYou rode with Godfrey\n1/3\n\nhttps " \
                   "://mail.google.com/mail/u/0/?ui=2&ik=23fb490d1a&view=pt&q=label %3Aspam esque% 20from %3Auber " \
                   "&qs=true&search=query&th= 15cO0890ad8e3bc5e&si...6/7/2017 Gmail - Your Sunday afternoon trip with " \
                   "Uber\n\n \n\n7.01 00:21:58 uberxX\nmiles Trip time Car\nRate Your Driver\nYour Fare\nTrip fare " \
                   "30.04\nSubtotal $30.04\n\nCHARGED\n(wea, Personal sees 5319 $30 . O04\n\nIssued by " \
                   "Rasier\nReceipt ID # cc8dd4f4-61f7-4ab2-918e-ce16ea70ea7a\n\nInvite your friends and family. " \
                   "Get\na free ride worth up to $15 when\nyou refer a friend to try Uber.\n\nShare code: 85asm\n\n " \
                   "\n\nhttps ://mail.google.com/mail/u/0/?ui=2&ik= 23fb490d1a&view=pt&q=label %3Aspam esque% 20from " \
                   "%3Auber &qs=true&search=query&th= 15cO0890ad8e3bc5e&si... 2/36/7/2017 Gmail - Your Sunday " \
                   "afternoon trip with Uber\n\nTap Help in your app to with\nquestions about your trip.\n\nLeave " \
                   "something behind?\n\nhttps ://mail.google.com/mail/u/0/?ui=2&ik= 23fb490d1a&view=pt&q=label " \
                   "%3Aspam esque% 20from %3Auber &qs=true&search=query&th= 15cO0890ad8e3bc5e&si... 3/3 "

        self.helper_function(ocr_text, 30.04, date.fromisoformat("2017-05-14"))

    def test_uber_parse_test_04(self):
        ocr_text = '6/7/2017\n\nM Gmail\n\nYour Wednesday evening trip with Uber\n\n1 message\n\nGmail - Your ' \
                   'Wednesday evening trip with Uber\n\n<firstname> <lastname> <testuser@gmail.com>\n\nWed, May 31, ' \
                   '2017 at 10:20 PM\n\nUber Receipts <uber.us@uber.com>\nTo: testuser+uber@gmail.com\n309 Washin ' \
                   'gton Fairmount\nH St NE Bennj. Heights\noN Seat Pleasant\nct Capitol SE\nCapitol (214\n- ' \
                   'Heights\nArlington % .\nS oe Walker Mi\nwld << Coral Hills\nOo\noad @ } Distric\n@) A e 8 SFX ' \
                   'Aiton, 218 a Height\nCrossrae x ¢ Ne “Amy, Suitland-Silver Hill\n3 é ls\n© = Hillcrest\noR, , ' \
                   'Heights €\nMap data ©2017 Google\n\n$15.08\n\n \n\nThanks for choosing Uber, <firstname>\n\nMay 31, ' \
                   '2017 |uberX\n\n® 10:03pm | 1 Aviation Cir, Arlington, VA\n\n@ 10:19pm | 2909 Zulu Ct, Washington, ' \
                   'DC\n\nYou rode with MBUNGU PATHY\n\nhttps ' \
                   '://mail.google.com/mail/u/0/?ui=2&ik=23fb490d1a&view=pt&q=label %3Aspam esque% 20from %3Auber ' \
                   '&qs=true&search=query&th= 15c6173dbb6a0bb0&si...\n\n1/36/7/2017 Gmail - Your Wednesday evening ' \
                   'trip with Uber\n\n \n\n6.06 00:16:22 uberxX\n\nmiles Trip time Car\nYour Fare\nTrip fare ' \
                   '15.08\nSubtotal $15.08\n\nCHARGED\n(wsa] Personal e*e* 5319 $ 1 5 “ O08\n\nIssued by ' \
                   'Rasier\nReceipt ID # 07a3fcdc-d78f-4d01 -8b27-d207a7841935\n\n& Invite your friends and family. ' \
                   'Get\n| a free ride worth up to $15 when\n| you refer a friend to try Uber.\n\nShare code: ' \
                   '85asm\n\n \n\nhttps ://mail.google.com/mail/u/0/?ui=2&ik= 23fb490d1a&view=pt&q=label %3Aspam ' \
                   'esque% 20from %3Auber &qs=true&search=query&th= 15c6173dbb6a0bb0&si... 2/36/7/2017 Gmail - Your ' \
                   'Wednesday evening trip with Uber\n\nTap Help in your app to with\nquestions about your ' \
                   'trip.\n\nLeave something behind?\n\nhttps ://mail.google.com/mail/u/0/?ui=2&ik= ' \
                   '23fb490d1a&view=pt&q=label %3Aspam esque% 20from %3Auber ' \
                   '&qs=true&search=query&th=15c6173dbb6a0bb0&si... 3/3 '
        self.helper_function(ocr_text, 15.08, date.fromisoformat("2017-05-31"))

    def test_uber_parse_test_05(self):
        ocr_text = '1/22/2019 Gmail - Your Thursday evening trip with Uber\n\nMm (small <firstname> <lastname> ' \
                   '<testuser@gmail.com>\n\nYour Thursday evening trip with Uber\n1 message\n\nUber Receipts ' \
                   '<uber.us@uber.com> Fri, Dec 7, 2018 at 12:11 AM\nTo: testuser+uber@gmail.com\n\nTotal: ' \
                   '$16.18\nThu, Dec 06, 2018\n\nThanks for riding,\n<firstname>\n\nWe hope you enjoyed your ride\nthis ' \
                   'evening.\n\nTotal $16.18\n\nTrip Fare $10.18\nSubtotal $10.18\nTolls, Surcharges, ' \
                   'and Fees $6.00\nAmount Charged\n\ne666 6779 Switch $16.18\n\nReceipt ID # ' \
                   '00d7f877-268b-43a0-a923-23e2e9e2c177\n\nhttps://mail.google.com/mail/u/0?7ik=23fb490d1a&view=pt' \
                   '&search=all&permthid=thread-f%3A1619168565382424456 1/3Gmail - Your Thursday evening trip with ' \
                   'Uber\n\n1/22/2019\nDownload PDF\n\nDownload link expires 1/6/19\n\nYou rode with Frances\nHow was ' \
                   'your ride?\n\n4.88 Rating\n\nTop Driver Compliment\n\n"Excellent Service"\n\nIssued by ' \
                   'Rasier\nWhen you ride with Uber, your trips are insured in case of a covered\n\naccident. Learn ' \
                   'more.\n\n5.89 mi | 16 min\n11:54pm (50)\n1 Aviation Cir, Arlington, VA\na\n12:10am\n1426 A St NE, ' \
                   'Washington,\nDC ws (238)\na\n8\ne vy\n{1} 5\n——" Pa\n\nMap data ©2018 Google\n2/3\n\n ' \
                   '\n\nhttps://mail.google.com/mail/u/0?ik=23fb490d1a&view=pt&search=all&permthid=thread-f' \
                   '%3A16191685653824244561/22/2019 Gmail - Your Thursday evening trip with Uber\n\nInvite your ' \
                   'friends and family.\n\nGet a free ride worth up to $5 when you refer a\n\nfriend to try Uber. ' \
                   'Share code: 85asm\n\nDriving Change Together\n\nWe\'ve partnered with Futures Without\nViolence ' \
                   'and more to help end\ngender-based violence in our\n\ncommunities.\n\nJOINUS >\n\nUber ' \
                   'Technologies\n1455 Market St\nSan Francisco, ' \
                   'CA 94103\n\nhttps://mail.google.com/mail/u/0?7ik=23fb490d1a&view=pt&search=all&permthid=thread-f' \
                   '%3A1619168565382424456 3/3 '
        self.helper_function(ocr_text, 16.18, date.fromisoformat("2018-12-06"))


if __name__ == '__main__':
    unittest.main()
