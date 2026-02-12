from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from tasks.models import Task
from .serializers import TaskSerializer, TaskUpdateSerializer
from tasks.permissions import IsUser, IsAdminOrSuperAdmin


class UserTaskList(APIView):
    permission_classes = [IsAuthenticated, IsUser]
    def get(self, request):
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class UpdateTaskStatus(APIView):
    permission_classes = [IsAuthenticated,IsUser]
    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, assigned_to=request.user)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)
        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class TaskReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]
    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, status='completed')
        except Task.DoesNotExist:
            return Response({"error": "Task not completed or not found"}, status=404)
        return Response({
            "title": task.title,
            "completion_report": task.completion_report,
            "worked_hours": task.worked_hours
        })
