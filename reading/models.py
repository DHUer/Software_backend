from django.db import models

class User(object):
    username = models.CharField(max_length = 20)
    mailbox = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)

