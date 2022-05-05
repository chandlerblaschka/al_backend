from calendar import weekday
from tkinter.messagebox import RETRY
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from psycopg2 import Date
# from rest_framework import viewsets
from .serializers import InputSerializer, MasterSerializer
from .models import Master, Input
# from rest_framework.permissions import AllowAny
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from datetime import date, datetime, timedelta
from django.db.models import Q

today = datetime.now().date()

if date.today().weekday() == 0:
    this_week = datetime.now() + timedelta(days=5)

if date.today().weekday() == 1:
    this_week = datetime.now() + timedelta(days=4)

if date.today().weekday() == 2:
    this_week = datetime.now() + timedelta(days=3)

if date.today().weekday() == 3:
    this_week = datetime.now() + timedelta(days=2)

if date.today().weekday() == 4:
    this_week = datetime.now() + timedelta(days=1)

if date.today().weekday() == 5 | 6:
    this_week = datetime.now() + timedelta(days=6)

@api_view(['GET', 'POST'])
def input(request):
    if request.method == 'GET':
        input_post = Input.objects.all()
        input_serializer = InputSerializer(input_post, many=True)
        return JsonResponse(input_serializer.data, safe=False)
    if request.method == 'POST':
        input_data = JSONParser().parse(request)
        input_serializer = InputSerializer(data=input_data)
        if input_serializer.is_valid():
            input_serializer.save()
            return JsonResponse(input_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def dashboard(request):
    if request.method == 'GET':
        all_actions = Master.objects.all()
        dashboard_serializer = MasterSerializer(all_actions, many=True)
        return JsonResponse(dashboard_serializer.data, safe=False)

@api_view(['GET'])
def dashboard_filter(request, industry=None, action=None):
    if request.method == 'GET':
        get_filter = Master.objects.filter(industry=industry, request=action.replace('-', ' '))
        get_filter_serializer = MasterSerializer(get_filter, many=True)
        return JsonResponse(get_filter_serializer.data, safe=False)

@api_view(['GET'])
def dashboard_table(request, year=None, month=None, action=None, employee=None):
    if request.method == 'GET':
        get_table = Master.objects.filter(Q(engineer=employee) | Q(sales=employee), dueDate__year=year, dueDate__month=month, request=action.replace('-', ' '))
        get_table_serializer = MasterSerializer(get_table, many=True)
        return JsonResponse(get_table_serializer.data, safe=False)
        
@api_view(['GET'])
def opportunity(request, oppNumber=None):
    if request.method == 'GET':
        get_opportunity = Master.objects.filter(oppNumber=oppNumber).order_by("request")
        get_opportunity_serializer = MasterSerializer(get_opportunity, many=True)
        return JsonResponse(get_opportunity_serializer.data, safe=False)

@api_view(['GET', 'POST'])
def industry(request, industry=None):
    if request.method == 'GET':
        industry_actions = Master.objects.filter(industry=industry).order_by("name", "oppNumber")
        industry_serializer = MasterSerializer(industry_actions, many=True)
        return JsonResponse(industry_serializer.data, safe=False)

    if request.method == 'POST':
        industry_data = JSONParser().parse(request)
        industry_serializer = MasterSerializer(data=industry_data)
        if industry_serializer.is_valid():
            industry_serializer.save()
            return JsonResponse(industry_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(industry_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view((['GET']))
def industry_open(request, industry):
    if request.method == 'GET':
        industry_open = Master.objects.filter(industry=industry, compDate=None).order_by("name", "oppNumber")
        industry_open_serializer = MasterSerializer(industry_open, many=True)
        return JsonResponse(industry_open_serializer.data, safe=False)

@api_view((['GET']))
def industry_today(request, industry):
    if request.method == 'GET':
        industry_today = Master.objects.filter(industry=industry, dueDate__lte=today, compDate=None).order_by("name", "oppNumber")
        industry_today_serializer = MasterSerializer(industry_today, many=True)
        return JsonResponse(industry_today_serializer.data, safe=False)

@api_view((['GET']))
def industry_this_week(request, industry):
    if request.method == 'GET':
        industry_this_week = Master.objects.filter(industry=industry, dueDate__lte=this_week, compDate=None).order_by("name", "oppNumber")
        industry_this_week_serializer = MasterSerializer(industry_this_week, many=True)
        return JsonResponse(industry_this_week_serializer.data, safe=False)

@api_view(['GET', 'PUT', 'DELETE'])
def edit_action(request, pk):
    try:
        edit_action = Master.objects.get(pk=pk)
    except Master.DoesNotExist:
        return JsonResponse({'message': 'This job does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        edit_action_serializer = MasterSerializer(edit_action)
        return JsonResponse(edit_action_serializer.data)

    elif request.method == 'PUT':
        edit_action_data = JSONParser().parse(request)
        edit_action_serializer = MasterSerializer(edit_action, data=edit_action_data)
        if edit_action_serializer.is_valid():
            edit_action_serializer.save()
            return JsonResponse(edit_action_serializer.data)
        return JsonResponse(edit_action_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        edit_action.delete()
        return JsonResponse({'message': 'Job was deleted successfully '})