from django.db import models

from django.contrib.auth.models import User #To connect Client model with user model

# Create your models here.
class Client (models.Model):
    user = models.OneToOneField(User, null =True, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200, null = True)
    phone = models.CharField(max_length = 200,null = True)
    email = models.EmailField(max_length = 200,null = True)
    # profile_pic = models.ImageField(null = True, blank=True)
    date_created = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return '%s %s' %(self.id, self.user)



#Rownok
class File(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    filename = models.CharField(max_length=200, null=True, blank = True, unique = True)
    file = models.FileField(null=True, blank = True, unique = True)
    review_column_name = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '%s %s' %(self.id, self.filename)



class Order(models.Model):
    STATUS = (
        ('Analyzed','Analyzed'),
        ('Pending', 'Pending'),
    )
    client = models.ForeignKey(Client,null = True, on_delete = models.SET_NULL)
    files = models.ForeignKey(File,null = True, on_delete = models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length = 50, null = True, choices = STATUS)

    def __str__(self):
        return 'Restaurant Name: %s,  File Id & Name: %s %s' %(self.client.name, self.files.id,  self.files.name)