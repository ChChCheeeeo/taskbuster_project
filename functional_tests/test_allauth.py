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

    # for google db
    fixtures = ['allauth_fixture']

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

    def user_login(self):
        # called afer clicking sign-in button
        import json
        with open("taskbuster_project/fixtures/google_user.json") as f:
            credentials = json.loads(f.read())
        for key, value in credentials.items():
            self.get_element_by_id(key).send_keys(value)
        for btn in ["signIn", "submit_approve_access"]:
            self.get_button_by_id(btn).click()
        return

    def test_google_login(self):
        self.browser.get(self.get_full_url("home"))
        # login present?
        google_login = self.get_element_by_id("google_login")
        print("google login is : ")
        print(google_login)
        # logout not present
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("logout")
            print("\nim in with statement for logout")
        # does login point to corrrect url?
        self.assertEqual(
            google_login.get_attribute("href"),
            self.live_server_url + "/accounts/google/login")
        # logout present afer clicking on logging in?
        google_login.click()
        print("google_login.click")
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("google_login")
            print("im in with statement google login")
        # logout, is login present again?
        google_logout = self.get_element_by_id("logout")
        print("google logout is: ")
        print(google_logout)
        google_logout.click()
        print("after logout click")
        self.user_login()
        print("after logging in with user_login")
        google_login = self.get_element_by_id("google_login")
        print("again google_login is ")
        print(google_login)


class TestTwitterLogin(StaticLiveServerTestCase):
    """TestTwitterLogin
    """
 
    fixtures = ['allauth_fixture']
 
    def setUp(self):
        self.browser = webdriver.WebDriver()
        self.browser.implicitly_wait(3)
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
 
    def user_login(self):
        import json
        with open("taskbuster/fixtures/twitter_user.json") as f:
            credentials = json.loads(f.read())
        for key, value in credentials.items():
            self.get_element_by_id(key).send_keys(value)
        for btn in ["allow"]:
            self.get_button_by_id(btn).click()
        return
 
    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)
 
    def test_twitter_login(self):
        self.browser.get(self.get_full_url("home"))
        twitter_login = self.get_element_by_id("twitter_login")
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("logout")
        self.assertEqual(
            twitter_login.get_attribute("href"),
            self.live_server_url + "/accounts/twitter/login")
        twitter_login.click()
        self.user_login()
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("twitter_login")
        logout = self.get_element_by_id("logout")
        logout.click()
        twitter_login = self.get_element_by_id("twitter_login")