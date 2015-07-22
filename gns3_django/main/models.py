from django.db import models
import datetime

class ServerSettings(models.Model):
	"""
		Server Settings stores the server url and port
		persistently in the database and loads it automatically
		when the app starts
	"""
	url = models.CharField('Server URL', max_length=200)
	port = models.IntegerField('Server Port')
	created_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.url + ':' + str(self.port)

class Project(models.Model):
    """
        Project Model stores the information
        for Projects
    """
    name = models.CharField('Project Name', max_length=200)
    project_id = models.CharField('Project ID', max_length=200)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name+"::"+self.project_id

class VCPS(models.Model):
    name = models.CharField('VCPS Name', max_length=200)
    project = models.ForeignKey(Project)
    vm_id = models.CharField('VM ID', max_length=200)
    udp_port = models.CharField('UDP Port', max_length=10)

    def __str__(self):
        return self.name+"::"+self.vm_id
