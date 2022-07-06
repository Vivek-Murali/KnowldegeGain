from curses.ascii import US
from django.contrib import admin
from .models import User, UserVisit, Profile

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(UserVisit)

# Register your models here.
