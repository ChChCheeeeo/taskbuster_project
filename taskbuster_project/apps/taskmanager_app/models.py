# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
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

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    # Django signal.
    # Should be read at the beginning of a Django app. Hence
    # why in models.py. Can place many signals in separate
    # file but import them early on.
    # User model signal triggered every time User instance is
    # saved.
    # sender: the User model class
    # created: a boolean indicating if a new User has been created
    # instance: the User instance being saved
    # arguments differ depending on the specific signal created. 
    # in this case, dealing with post_save signal

    if created:
        profile = Profile(user=instance)
        profile.save()


class Project(models.Model):
    """Project
    """
    # From project instance, named myproject, can obtain its related 
    # profile with:  myproject.user
    # note attribute name defined in Project is user and not 
    # profile.

    # From profile instance, named myprofile, can obtain its related 
    # projects with:  myprofile.projects.all() .
    # Without specifying a related_name, by default access projects 
    # of a profile with myprofile.project_set.all() .
    # Note myprofile.project returns an object manager, so to obtain 
    # project instances, use query methods, like all(), filter(), exclude(), etc. We could even call the custom methods defined in the custom ProjectManager class.



    # Relations
    user = models.ForeignKey(
        # each project instance must relate to one User Profile (profile
        # field mandatory) and each User Profile can be related to 0, 1, 
        # or more projects
        Profile,
        related_name="projects",
        verbose_name=_("user")
    )
    
    # Attributes - Mandatory
    name = models.CharField(
        max_length=100,
        verbose_name=_("name"),
        help_text=_("Enter the project name")
    )
    
    color = models.CharField(
        max_length=7,
        # hex colors between #000000 and #FFFFFF
        # double pair can be abbreviated
        # #001122 --> #012
        default="#fff",
        validators=[RegexValidator(
        "(^#[0-9a-fA-F]{3}$)|(^#[0-9a-fA-F]{6}$)")],
        verbose_name=_("color"),
        help_text=_("Enter the hex color code, like #ccc or #cccccc")
    )

    # Attributes - Optional
    # Object Manager
    # Custom object manager.
    objects = managers.ProjectManager()
    # Custom Properties
    # Methods

    # Meta and String
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ("user", "name")
        # define at the db level, that for the same profile, can't
        # write two projects to the same name. 
        unique_together = ("user", "name")

    def __str__(self):
        return "%s - %s" % (self.user, self.name)