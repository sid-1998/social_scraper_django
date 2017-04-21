# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# class ModelUser(models.Model):
#     user = models.OneToOneField(User)

class Codechef(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    username = models.CharField(max_length=30, default="", blank=True)
    name = models.CharField(max_length=30, default="", blank=True)
    country = models.CharField(max_length=30, default="", blank=True)
    rating = models.CharField(max_length=30, default="", blank=True)
    globalRank = models.CharField(max_length=30, default="", blank=True)
    countryRank = models.CharField(max_length=30, default="", blank=True)

class Quora(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    username = models.CharField(max_length=30, default="", blank=True)
    answers = models.CharField(max_length=30, default="", blank=True)
    monthViews = models.CharField(max_length=30, default="", blank=True)
    totalViews = models.CharField(max_length=30, default="", blank=True)
    name = models.CharField(max_length=30, default="", blank=True)
