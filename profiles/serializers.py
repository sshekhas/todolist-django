from rest_framework import serializers
from profiles.models import TodoList
from authentication.serializers import UserDetailsSerializer


class TodoListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TodoList
        fields = "__all__"


    def validate(self, data):
        data["user"] = self.context["request"].user
        return super().validate(data)


class TaskDetailsSerializer(serializers.Serializer):
    name = serializers.CharField()
    done_task = serializers.IntegerField()
    pending_task = serializers.IntegerField()
    urgent_task = serializers.IntegerField()
    total_task = serializers.IntegerField()
