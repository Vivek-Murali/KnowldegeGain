from django.urls import path
from django.conf.urls import url
from .views import COREFetch, create_todo


urlpatterns = [
    path('FetchRecordsFromKey/', COREFetch.as_view(), name='COREFetch'),
    path('create/', create_todo, name='create-todo'),
]
