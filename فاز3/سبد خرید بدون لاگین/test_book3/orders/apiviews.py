from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import TaskSerializer
from json_excel_converter import Converter
from json_excel_converter.xlsx import Writer


class OrdersList(APIView):
    """
    get request from user and save data from serializer to json,
    then show all order to user with APIView.

    Note:
    for download as json use first method.
    for download as excel use second method.

    """

    # def get(self, request):
    #     """for json file"""
    #     now = datetime.now().day
    #     # tasks = Invoice.objects.all()[:20]
    #     tasks = Invoice.objects.all().filter(created__day=now)[:20]
    #     data = TaskSerializer(tasks, many=True).data
    #     return Response(data)

    # def get_exel(self, request):
    def get(self, request):  # for run
        """
        convert json file to exel
        """
        import pandas as pd
        now = datetime.now().day
        tasks = Invoice.objects.all().filter(created__day=now)[:20]
        json_file = TaskSerializer(tasks, many=True).data
        # data = pd.DataFrame(json_file).to_excel("excel.xlsx")
        # return pd.DataFrame(json_file).to_excel("excel.xlsx")  # save in local
        return Response(pd.DataFrame(json_file).to_excel("excel.xlsx"))


class AllOrdersList(APIView):
    """
    get request from user and save data from serializer to json,
    then show all order to user with APIView.
    """

    def get(self, request):
        """for json file"""
        now = datetime.now().day
        tasks = Invoice.objects.all()
        data = TaskSerializer(tasks, many=True).data
        return Response(data)


class OrdersDetail(APIView):
    """get request from user with pk and save data from serializer to json,
    then show details one order to user with APIView."""

    def get(self, request, pk):
        task = get_object_or_404(Invoice, pk=pk)
        data = TaskSerializer(task).data
        return Response(data)
