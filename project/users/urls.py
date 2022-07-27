from django.urls import include, path
from .views import COREFetch, CORETimeline, COREVennDiagram

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('v1/FetchRecordsFromKey/', COREFetch.as_view(), name='COREFetch'),
    path('v1/FecthRecordsWithTimeline/',CORETimeline.as_view(), name='CORETimeline'),
    path('v1/VennDiagramData/',COREVennDiagram.as_view(), name='COREVennDiagram'),
]
