# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render, HttpResponse
from django.conf import settings
from . import reddit_flair_prediction as rdf
import sys
import pickle
import pandas as pd
# Create your views here.
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import FileSerializer
from .models import *
import csv
import json
from django.http import FileResponse

class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def get(self, request):
        upload_file = File.objects.all()
        serializer = FileSerializer(upload_file, many = True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        file_serializer = FileSerializer(data=request.data)
        fl = request.data
        fl = fl['upload_file']
        dat = fl.readlines()

        res = {}

        for line in dat:
            url = line.decode('utf-8')
            flair = rdf.detect_flair(url)[0]
            res[url] = str(flair)
        fp = open('res.json', 'w')
        json.dump(res, fp)
        fp.close()

        if file_serializer.is_valid():
            file_serializer.save()
            # return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            response = FileResponse(open('res.json', 'rb'))
            return response
        else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def index(request):

    if request.method == 'POST':
        val = request.POST.get('url')
        return render(request,"flair_detector/index.html",{"output":rdf.detect_flair(val)[0]})
    return render(request,"flair_detector/index.html")

sys.stdout.flush()
