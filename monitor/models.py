# -*- coding: utf-8 -*-
from django.db import models, connection

class DrawTreeManager(models.Manager):
    def getclass(self, sql):
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
 
class DrawTree(models.Model):
    classname = models.CharField(max_length=64)
    hostname = models.CharField(max_length=64)
    hostid = models.CharField(max_length=8)
    graphid = models.CharField(max_length=8)
    graphname = models.CharField(max_length=128)
    draw = models.CharField(max_length=2)
    type = models.CharField(max_length=2)
    objects = DrawTreeManager()
    def __unicode__(self):
        return self.hostname
 
################################################
class DrawGraphsManager(models.Manager):
    def getdata(self, sql):
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
 
class DrawGraphs(models.Model):
    graphid = models.CharField(max_length=8)
    itemid = models.CharField(max_length=8)
    itemname = models.CharField(max_length=128)
    units = models.CharField(max_length=16, null=True, blank=True)
    objects = DrawGraphsManager()
    def __unicode__(self):
        return self.graphid
 
#################################################
class DrawDefManager(models.Manager):
    def getdata(self, sql):
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
 
class DrawDef(models.Model):
    graphid = models.CharField(max_length=8)
    cols = models.CharField(max_length=256, null=True, blank=True)
    types = models.CharField(max_length=256, null=True, blank=True)
    objects = DrawDefManager()
    def __unicode__(self):
        return self.graphid
