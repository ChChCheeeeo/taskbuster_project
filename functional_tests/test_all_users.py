# -*- coding: utf-8 -*-
#from django.contrib.staticfiles.testing import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import activate
from django.core.urlresolvers import reverse
from django.utils import formats

from selenium.webdriver.firefox import webdriver

from datetime import date

#import unittest



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
        activate('en')

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

    def test_home_files(self):
        # check when going to corresponding url that 
        # Not Found 404 page doesn't show up.
        self.browser.get(self.live_server_url + "/robots.txt")
        self.assertNotIn("Not Found", self.browser.title)
        self.browser.get(self.live_server_url + "/humans.txt")
        self.assertNotIn("Not Found", self.browser.title)

    def test_internationalization(self):
        for lang, h1_text in [('en', 'Welcome to TaskBuster!'),
            ('ca', 'Benvingut a TaskBuster!')]:
            activate(lang)
            self.browser.get(self.get_full_url("home"))
            h1 = self.browser.find_element_by_tag_name("h1")
            self.assertEqual(h1.text, h1_text)

    def test_localization(self):
        today = date.today()
        for lang in ['en', 'ca']:
            activate(lang)
            self.browser.get(self.get_full_url("home"))
            local_date = self.browser.find_element_by_id("local-date")
            non_local_date = self.browser.find_element_by_id("non-local-date")
            self.assertEqual(formats.date_format(today, use_l10n=True),
                                  local_date.text)
            self.assertEqual(today.strftime('%Y-%m-%d'), non_local_date.text)