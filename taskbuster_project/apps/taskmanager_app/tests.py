# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase

from . import models


class TestProfileModel(TestCase):
    """TestProfileModel
    """

    def test_profile_creation(self):
        # get_user_model returns custom user model if it
        # exists or default Django model is it doesnt. 
        User = get_user_model()
        # New user created
        user = User.objects.create(
            unique=True,
            username="taskbuster",
            password="django-tutorial"
        )
        # Check that a Profile instance has been crated
        self.assertIsInstance(user.profile, models.Profile)
        # Call the save method of the user to activate the 
        # signal again, and check that it doesn't try to 
        # create another profile instace
        user.save()
        self.assertIsInstance(user.profile, models.Profile)

class TestProjectModel(TestCase):
    """TestProjectModel
    """

    def setUp(self):
        User = get_user_model()
        # user instance fires a signal that creates a related profile
        # instance
        # both saved for later use.
        self.user = User.objects.create(
            username="taskbuster", 
            password="django-tutorial"
        )
        self.profile = self.user.profile

    def tearDown(self):
        # delete user instance. doing so also deletes all related
        # instances that depend onthis one: profile depends on user,
        # project depends on the profile. 
        self.user.delete()

    def test_validation_color(self):
        # This first project uses the default value, #fff
        # test difference color inputs
        project = models.Project(
            user=self.profile,
            name="TaskManager"
        )
        self.assertTrue(project.color == "#fff")
        # using default value, Validation shouldn't rise an Error
        # call full_clean as calling saving the method won't work.
        project.full_clean()

        # Good color inputs (without Errors):
        for color in ["#1cA", "#1256aB"]:
            project.color = color
            project.full_clean()

        # Bad color inputs:
        for color in ["1cA", "1256aB", "#1", "#12", "#1234", "#12345", "#1234567"]:
            with self.assertRaises(
                ValidationError,
                msg="%s didn't raise a ValidationError" % color):
                project.color = color
                project.full_clean()