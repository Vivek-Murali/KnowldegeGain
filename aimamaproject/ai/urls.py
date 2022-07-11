from django.urls import path
from django.conf.urls import url
from .views import COREFetch


urlpatterns = [
    path('FetchRecordsFromKey/', COREFetch.as_view(), name='COREFetch'),
]
