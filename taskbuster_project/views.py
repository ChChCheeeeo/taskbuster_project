# -*- coding: utf-8 -*-
from django.utils.timezone import  now
from django.shortcuts import render

import datetime


def home(request):
    today = datetime.date.today()
    return render(request, "taskbuster_project/index.html",
        {
            'today': today,
            'now': now(),
        }
    )

def home_files(request, filename):
    return render(request, filename, {}, content_type="text/plain")