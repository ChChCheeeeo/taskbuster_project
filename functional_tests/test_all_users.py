# -*- coding: utf-8 -*-
#from django.contrib.staticfiles.testing import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse

from selenium.webdriver.firefox import webdriver
import unittest

# LiveServerTestCase doesn't support static files
#class HomeNewVisitorTest(LiveServerTestCase):#unittest.TestCase):
class HomeNewVisitorTest(StaticLiveServerTestCase):
    """NewVisitorTest
    """

    # setUp and tearDown run before and after every
    # test_
    def setUp(self):
        self.browser = webdriver.WebDriver()#Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def get_full_url(self, namespace):
        # gives local host url
        # use this method because test server uses another url
        # reverse gives relative url of a given namespace here /
        # resulting function gives the absolute url of that 
        # namespace (the sum of the previous two), 
        return self.live_server_url + reverse(namespace)

    def test_home_title(self):
        self.browser.get(self.get_full_url("home"))
        self.assertIn("TaskBuster", self.browser.title)

    def test_h1_css(self):
        # The css rule for the text color will be on a CSS 
        # file, which means that if the test passes, 
        # staticfiles are loading correctly.
        self.browser.get(self.get_full_url("home"))
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(
            h1.value_of_css_property("color"),
            "rgba(200, 50, 255, 1)"
        )
