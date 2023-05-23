# profiles/urls.py

from django.urls import path, include
from rest_framework import routers
from profiles.views import TodoListViewSet, TaskDetailsView




router = routers.DefaultRouter()
router.register("todo-list", TodoListViewSet)

urlpatterns = [

    path("", include(router.urls)),
    path("task-details/", TaskDetailsView.as_view())
]