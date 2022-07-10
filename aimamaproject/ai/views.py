from django.shortcuts import render
from django.http import JsonResponse
#from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg import openapi
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
import logging
import numpy as np
import json
import uuid
import os
import requests



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


# Create your views here.
