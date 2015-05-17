# -*- coding: utf-8 -*-
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.common.by import By

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.utils.translation import activate


class TestGoogleLogin(StaticLiveServerTestCase):
    """TestGoogleLogin
    """

    def setUp(self):
        self.browser = webdriver.WebDriver()
        self.browser.implicitly_wait(3)
        # wait some time before raising exception if element
        # not found
        self.browser.wait = WebDriverWait(self.browser, 10)
        activate('en')

    def tearDown(self):
        self.browser.quit()

    def get_element_by_id(self, element_id):
        return self.browser.wait.until(EC.presence_of_element_located(
                (By.ID, element_id)))

    def get_button_by_id(self, element_id):
        return self.browser.wait.until(EC.element_to_be_clickable(
                (By.ID, element_id)))

    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)

    def test_google_login(self):
        self.browser.get(self.get_full_url("home"))
        # login present?
        google_login = self.get_element_by_id("google_login")
        # logout not present
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("logout")
        # does login point to corrrect url?
        self.assertEqual(
            google_login.get_attribute("href"),
            self.live_server_url + "/accounts/google/login")
        # logout present afer clicking on logging in?
        google_login.click()
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("google_login")
        # logout, is login present again?
        google_logout = self.get_element_by_id("logout")
        google_logout.click()
        google_login = self.get_element_by_id("google_login")