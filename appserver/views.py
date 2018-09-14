# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from similar_predict import *

class SimilarPredict(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated, )
	authentication_classes = (JSONWebTokenAuthentication, )

	def post(self, request, format=None):
		# Assign the created by user
		data = {}
		data['title'] =  request.data['title']
		data['production'] = request.data['production']
		data['release_year'] = request.data['release_year']
		data['genre1'] = request.data['genre1']
		data['genre2'] = request.data['genre2']
		data['genre3'] = request.data['genre3']
		data['director1'] = request.data['director1']
		data['director2'] = request.data['director2']
		data['actor1'] = request.data['actor1']
		data['actor2'] = request.data['actor2']
		data['actor3'] = request.data['actor3']
		data['budget'] = request.data['budget']
		data['production_country'] = request.data['production_country']

		resp = get_similar(request, **data)
		# resp = True
		return Response(resp, status=status.HTTP_201_CREATED)
