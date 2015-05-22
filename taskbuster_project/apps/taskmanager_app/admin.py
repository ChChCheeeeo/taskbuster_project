# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models


# register ProfileAdmin as ModelAdmin of the Profile-Model
# (where admin instance to the model to manage is connected)
# @admin.register(models.Profile)
# class ProfileAdmin(admin.ModelAdmin):
#    """ProfileAdmin
#    """
    # defile ProfileAdmin as modelAdmin instance

    # define fields displayed when listing profile instances.
    # in admin, two columns seen: username, and interaction
    # since custom attribute usernamed defined, can use 
    # username instead of user__username
#   list_display = ("username", "interaction")

    # create search box. field list specify which fields
    # are searched
    # for search field, need to use a normal model attribute
    # so use user__username instead of username.
#    search_fields = ["user__username"]


class ProjectsInLine(admin.TabularInline):
    """ProjectsInLine
    """
    model = models.Project
    # how many extra Projects should appear when editing a Profile insstanc.

    extra = 0


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    """ProfileAdmin
    """

    list_display = ("username", "interaction", "_projects")

    search_fields = ["user__username"]

    # Note that when creating a new project inside a profile instance, 
    # the relation between both objects is automatically set 
    # (don’t need to specify the profile field in the project instance).
    # only Projects related to the current profile instance are shown 
    # in the admin site..
    inlines = [
        ProjectsInLine
    ]

    def _projects(self, obj):
        return obj.projects.all().count()