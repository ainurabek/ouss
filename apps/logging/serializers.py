from rest_framework import serializers
from apps.logging.models import ActivityLogModel
from apps.accounts.serializers import UserLogSerializer


class ActivityLogSerializer(serializers.ModelSerializer):
    action_by = UserLogSerializer()
    class Meta:
        model = ActivityLogModel
        fields = ('id', 'action_by', 'action_description', 'action_time')