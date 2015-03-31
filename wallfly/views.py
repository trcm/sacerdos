from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

from wallfly.models import *
from wallfly.serializers import PropertySerializer

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.core import serializers


def home(request):
    return render(request, 'base.djhtml')


class PropertyView(APIView):

    def get(self, request, format=None):
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)

        return Response(serializer.data)
