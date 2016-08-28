from django.db import models
from django.utils.timezone import localtime
import datetime

# Create your models here.
class Player(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return str(self.name)

class Map(models.Model):
	map_name = models.CharField(max_length=100)
	def __str__(self):
		return self.map_name
	class Meta:
		ordering = ['map_name']

class Result(models.Model):
	class Meta:
		ordering = ['-date']
	won = models.BooleanField()
	played_with = models.ManyToManyField(Player,blank=True)
	date = models.DateTimeField(auto_now_add=True)
	map_played = models.ForeignKey(Map, null=True)
	comments = models.TextField(null=True, blank=True)
	def __str__(self):
		winstring = "Victory " if self.won else "Defeat "
		return winstring + "on " + (str(self.map_played) or "") + \
				' with ' + ' '.join([str(p) for p in self.played_with.all()]) + \
				 " at " + str(datetime.datetime.strftime(localtime(self.date),"%Y-%m-%d %H:%M:%S"))