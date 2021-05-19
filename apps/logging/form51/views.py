# coding: utf-8
from apps.accounts.models import Profile
from apps.logging.models import ActivityLogModel
from .constants import FORM51_LOG_DESCRIPTIONS
from apps.opu.form51.models import Form51
from datetime import datetime



class Form51LogUtil:
    def __init__(self, action_by, action_applied_to_object):
        self.action_by = Profile.objects.get(user=action_by)
        self.action_applied_to_object = Form51.objects.get(pk=action_applied_to_object)
        self.action_time = datetime.now()

    def form51_create_action(self, action):
        ActivityLogModel.objects.create(
            action_by=self.action_by,
            action_description=FORM51_LOG_DESCRIPTIONS[action]
                               % (
                                  self.action_applied_to_object.object.name,
                                  self.action_applied_to_object.object.id_outfit.outfit,
                                  ),
            action_time=self.action_time
        )

