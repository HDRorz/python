#coding=utf-8
from django.db import models
from django.contrib.auth.models import User, UserManager
from datetime import datetime
import time
import pytz 
from django.conf import settings

#扩展user类？
class Users(User):
    nickname    = models.CharField(max_length = 40)
    objects     = UserManager()
    #dobjects = models.manager.Manager()
    #def __unicode__(self):
        #return u"<Users: %s %s %s >" % (self.username, self.nickname, self.name)
