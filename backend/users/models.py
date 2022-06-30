from django.db import models
from djongo import models


# Create your models here.
class Articles(models.Model):
    article_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    tagline = models.TextField()
    domain = models.CharField(max_length=100)

    class Meta:
        abstract = True
        
class Associations(models.Model):
    user_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True
        

class User(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length = 254)
    occupation = models.CharField(max_length=150,null=True)
    username = models.CharField(max_length=25)
    phoneno = models.CharField(max_length=10)
    extension = models.CharField(max_length=3)
    location = models.CharField(max_length=100)
    gender = models.CharField(choices=[('Male','Male'),('Female','Female'),('Others','Others')], default="Male", max_length=6)
    associations = models.EmbeddedField(
        model_container=Associations,null=True, blank=True
    )
    active = models.BooleanField(default=False)
    published = models.EmbeddedField(
        model_container=Articles,null=True, blank=True
    )
    liked_article = models.EmbeddedField(
        model_container=Articles, null=True, blank=True
    )
    headline = models.CharField(max_length=255)    
    objects = models.DjongoManager()