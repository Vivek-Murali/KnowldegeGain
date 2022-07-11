from django.shortcuts import render
from django.http import JsonResponse
#from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg import openapi
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from .serializer import (TextSerializer, OpenAPISerializer)
from datetime import datetime
import logging
import numpy as np
import json
from bson.objectid import ObjectId
import uuid
import os
import requests
from django.conf import settings
from .src import main

from .forms import TodoForm
from .models import Todo
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


logging.basicConfig(format='%(levelname)-s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%s')


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)
        
        
class COREFetch(GenericAPIView):  # generics.CreateAPIView
    # permission_classes = (Check_API_KEY_Auth,)
    serializer_class = TextSerializer
    
    login_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'Text': openapi.Schema(type=openapi.TYPE_STRING, description='Keyword to search for finidng associations'),
            'Key': openapi.Schema(type=openapi.TYPE_STRING, description='16 Chars long Private Key'),
        },
        required=['Text', 'Key']
    )
    
    login_schema_response = {
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'RawText': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        status.HTTP_201_CREATED: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'RawText': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'RawText': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
    }

    @swagger_auto_schema(request_body=login_schema, responses=login_schema_response)
    def post(self, request):
        """
        This text is the description for this API.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        text = data['Text']
        request_id = data['Key']
        objInstance = ObjectId(request_id)
        if text == '':
            return Response("Got Empty String", status=status.HTTP_500_BAD_REQUEST)
        Database = settings.MONGO.find_one(collection='userapp_profile',query={'_id':objInstance}) #62cb0800822bd4f866bb1284
        if Database:
            rows = settings.CASSANDRA.query_topics(collection="datasource_core",keywords=text,limit=100)
            records = main.mapsets(list(rows))
            response_dict = {"RawText": text, "ProcessedData": records,
                        'ProcessedDate': datetime.utcnow().__str__(),
                        "RequestID": request_id, "status": 200,
                        "Version": settings.VERSION}
            return JsonResponse(response_dict, status=200)
        else:
            response_dict = {"Error": {"Reason": "Unauthorized Access, Please Use The Right Key"}}
            return JsonResponse(response_dict,status=401)


@login_required
def create_todo(request):
    form = TodoForm()
    context = {'form': form}

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)

        todo = Todo()

        todo.title = title
        todo.description = description
        todo.is_completed = True if is_completed == "on" else False
        todo.owner = request.user
        todo.save()

        messages.add_message(request, messages.SUCCESS, "Todo created successfully")

        return HttpResponseRedirect(reverse("todo", kwargs={'id': todo.pk}))

    return render(request, 'todo/create-todo.html', context)
# Create your views here.
