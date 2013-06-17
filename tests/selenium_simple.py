import unittest
from selenium import webdriver

class TestUbuntuHomepage(unittest.TestCase):

     def setUp(self):
         print "21.0 Firefox on Ubuntu is a little buggy. Check 'firefox' from command line.\n Got 'GLib-CRITICAL **: g_slice_set_config: assertion sys_page_size == 0 failed' error."
         self.browser = webdriver.Firefox()

     def testTitle(self):
         self.browser.get('http://www.ubuntu.com/')
         self.assertIn('Ubuntu', self.browser.title)

     def tearDown(self):
         self.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)
