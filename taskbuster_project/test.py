# -*- coding: utf-8 -*-
from django.utils.translation import activate
from django.core.urlresolvers import reverse
from django.test import TestCase


class TestHomePage(TestCase):
    """TestHomePage
    """

    def test_uses_index_template(self):
        activate('en')
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, 
            "taskbuster_project/index.html")

    def test_uses_base_template(self):
        activate('en')
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "base.html")