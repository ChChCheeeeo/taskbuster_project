# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from . import managers


class Profile(models.Model):
    """Profile
    """
    # Relations
    user = models.OneToOneField(
        # User model imported with AUTH_USER_MODEL from
        # settings.py Cause sometimes you want to define
        # custom model thus model should have a one-to-one
        # relationsihp with custome user model isntead of
        # Django-profivded built-in model.
        settings.AUTH_USER_MODEL,
        # define how you access a profile instance from the
        # user model. Ex: myuser is User instance, access its
        # profile with myprofile = myuser.profile. However for
        # a one-to-one relationship, django uses the acces key
        # by default (class name in lowercase). 
        related_name="profile",
        # define more readable name. Note it's wrapped around
        # ugettext_lazy fucntion. Used to translate string if
        # translation available. 
        verbose_name=_("user")
    )

    # Attributes - Mandatory
    interaction = models.PositiveIntegerField(
        default=0,
        verbose_name=_("interaction")
    )

    # Attributes - Optional
    # Object Manager
    # used to make queries. Custom object managers allow to 
    # define custom functions to make queries. 
    objects = managers.ProfileManager()

    # Custom Properties
    @property
    def username(self):
        # now can access using profile.username. it wont create
        # a row in db table (so it's differnt than a model
        # attribute).
        # As a custom property, it wont touch db, thus can 
        # change without having to migrate code.
        return self.user.username

    # Methods

    # Meta and String
    class Meta:
        # defile other model behaviors.
        # verbose_name and verbose_name_plural model
        # user-friendly names
        # ordering defines how model orders queries in 

        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("user",)

        def __str__(self):
            return self.user.username