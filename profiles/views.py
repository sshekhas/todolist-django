from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from profiles.models import TodoList
from profiles.serializers import TodoListSerializer, TaskDetailsSerializer
from profiles.filters import TodoListFilter

# Create your views here.

class TodoListViewSet(ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer

    permission_classes = [IsAuthenticated]

    filterset_class = TodoListFilter

    def get_queryset(self):
        if not self.request.user.is_staff:
            return super().get_queryset().filter(user=self.request.user).order_by("date")
        return super().get_queryset()
    

class TaskDetailsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        name = f"{user.first_name} {user.last_name}"
        todos = list(TodoList.objects.filter(user=user))
        done_task = 0
        pending_task = 0
        urgent_task = 0
        total_task = 0
        for task in todos:
            total_task += 1
            if task.is_done:
                done_task += 1
            else:
                pending_task += 1
            if task.is_urgent:
                urgent_task += 1
        
        serializer = TaskDetailsSerializer(
            data={
                    "name": name,
                    "done_task": done_task,
                    "pending_task": pending_task,
                    "urgent_task": urgent_task,
                    "total_task": total_task,
                }
        )
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response
