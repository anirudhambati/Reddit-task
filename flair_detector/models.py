# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class File(models.Model):
    upload_file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.upload_file.name
