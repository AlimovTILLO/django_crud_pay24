from django.db import models

# Create your models here.
class Passport(models.Model):
    firstname = models.CharField(max_length=32)
    lastname = models.CharField(max_length=32)
    middlename = models.CharField(max_length=32)
    phone = models.IntegerField()
    address = models.CharField(max_length=54)
    tin = models.BinaryField()
    

    def __str__(self):
        return "%s - %s - %s" % (self.firstname,  self.lastname, self.middlename)
    class Meta:
        db_table = 'passport'