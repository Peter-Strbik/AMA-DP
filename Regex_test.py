# -*- coding: utf-8 -*-
import unittest
from utils import who, when


class RegexTest(unittest.TestCase):
    def setUp(self):
        print "Testing now"
    def tearDown(self):
        print "Done Testing"
    def test1_name(self):
        r = who("Who was Walt Whitman?")
        self.assertEqual(r, "Walt Whitman")
    def test2_name(self):
        r = who("Who is Dennis Yatunin?")
        self.assertEqual(r, "Dennis Yatunin")
    def test3_name(self):
        r = who("Who is Barack H. Obama?")
        self.assertEqual(r, "Barack H. Obama")
    def test4_name(self):
        r = who("Who likes Tasty Apple Cider?")
        self.assertEqual(r, "Tasty Apple Cider")
    def test5_name(self):
        r = who("Who was Baron Wolfgang von Strucker?")
        self.assertEqual(r, "Baron Wolfgang von Strucker")
    def test6_name(self):
        r = who("Who was Luther O'Neil McCormick?")
        self.assertEqual(r, "Luther O'Neil McCormick")
    def test7_name(self):
        r = who("Who omg is omg His Royal Highness Q. Q. Oh-So-Tasty Apple Cider omg omg omg?")
        self.assertEqual(r, "His Royal Highness Q. Q. Oh-So-Tasty Apple Cider")
    def test8_name(self):
        r = who(u"Who was Björk Guðmundsdóttir?")
        self.assertEqual(r, u"Björk Guðmundsdóttir")
    def test9_name(self):
        r = who(u"ayeee Dies Ist Äußerst Köstliche Apfelwein")
        self.assertEqual(r, u"Dies Ist Äußerst Köstliche Apfelwein")
    def test10_name(self):
        r = who(u"Who is this weirdo Nguyễn Tấn Dũng?")
        self.assertEqual(r, u"Who is this weirdo Nguyễn Tấn Dũng?")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(RegexTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

    
