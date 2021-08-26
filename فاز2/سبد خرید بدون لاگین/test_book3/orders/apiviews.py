from datetime import timezone

from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import TaskSerializer
import pandas as pd


class TaskList(APIView):
    """
    get request from user and save data from serializer to json,
    then show all order to user with APIView.
    """

    def get(self, request):
        """
        return json file
        """
        now = datetime.now().day
        # tasks = Invoice.objects.all()[:20]
        tasks = Invoice.objects.all().filter(created__day=now)[:20]
        data = TaskSerializer(tasks, many=True).data
        return Response(data)

    # def get(self, request):
    def get_exel(self, request):
        """
        convert json file to exel
        """
        now = datetime.now().day
        tasks = Invoice.objects.all().filter(created__day=now)[:20]
        json_file = TaskSerializer(tasks, many=True).data
        # data = pd.DataFrame(json_file).to_excel("excel.xlsx")
        # return pd.DataFrame(json_file).to_excel("excel.xlsx")  # save in local
        return Response(pd.DataFrame(json_file).to_excel("excel.xlsx"))


class TaskDetail(APIView):
    """get request from user with pk and save data from serializer to json,
    then show details one task to user with APIView."""

    def get(self, request, pk):
        task = get_object_or_404(Invoice, pk=pk)
        data = TaskSerializer(task).data
        return Response(data)

# class TaskList2(APIView):
#     def get(self, request):
#         tasks = Task.objects.all()[:20]
#         serializer = TaskSerializer(tasks, many=True)
#         return Response({'tasks': serializer.data})
