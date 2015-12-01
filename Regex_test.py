# -*- coding: utf-8 -*-
import unittest
from utils import who, when


class RegexTest(unittest.TestCase):
    def setUp(self):
        print "Testing now"
    def tearDown(self):
        print "Done Testing"
    def test1_name(self):
        r = who("Tell me about Walt Whitman.")
        self.assertEqual(r, "Walt Whitman")
    def test2_name(self):
        r = who("Tell me about Dennis Yatunin.")
        self.assertEqual(r, "Dennis Yatunin")
    def test3_name(self):
        r = who("Tell me about Barack H. Obama.")
        self.assertEqual(r, "Barack H. Obama")
    def test4_name(self):
        r = who("Tell me about Tasty Apple Cider.")
        self.assertEqual(r, "Tasty Apple Cider")
    def test5_name(self):
        r = who("Tell me about Baron Wolfgang von Strucker.")
        self.assertEqual(r, "Baron Wolfgang von Strucker")
    def test6_name(self):
        r = who("Tell me about Luther O'Neil McCormick.")
        self.assertEqual(r, "Luther O'Neil McCormick")
    def test7_name(self):
        r = who("Tell me about His Royal Highness Q. Q. Oh-So-Tasty Apple Cider.")
        self.assertEqual(r, "His Royal Highness Q. Q. Oh-So-Tasty Apple Cider")
    def test8_name(self):
        r = who(u"Tell me about Björk Guðmundsdóttir.")
        self.assertEqual(r, u"Björk Guðmundsdóttir")
    def test9_name(self):
        r = who(u"Tell me about Dies Ist Äußerst Köstliche Apfelwein.")
        self.assertEqual(r, u"Dies Ist Äußerst Köstliche Apfelwein")
    def test10_name(self):
        r = who(u"Tell me about this weirdo Nguyễn Tấn Dũng.")
        self.assertEqual(r, u"Tell me about this weirdo Nguyễn Tấn Dũng.")
    def test11_name(self):
        r = who(u"Tell me about this guy 王宜成.")
        self.assertEqual(r, u"Tell me about this guy 王宜成.")
    def test12_name(self):
        r = when(u"Tell me about 22-11-15.")
        self.assertEqual(r, u"22-11-15")
    def test12_name(self):
        r = when(u"Tell me about 30/Feb/2000.")
        self.assertEqual(r, u"Tell me about 30/Feb/2000.")
    def test13_name(self):
        r = when(u"Tell me about 29/Feb/2000.")
        self.assertEqual(r, u"29/Feb/2000")
    def test14_name(self):
        r = when(u"Tell me about Feb/29/2000.")
        self.assertEqual(r, u"Feb/29/2000")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(RegexTest)
    unittest.TextTestRunner(verbosity=2).run(suite)


