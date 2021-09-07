# coding: utf-8
from apps.accounts.models import Profile
from apps.logging.models import ActivityLogModel
from .constants import FORM53_LOG_DESCRIPTIONS, FORM53_LOG_DELETE_DESCRIPTIONS
from apps.opu.form53.models import Form53




class Form53LogUtil:
    def __init__(self, action_by, action_applied_to_object):
        self.action_by = Profile.objects.get(user=action_by)
        self.action_applied_to_object = Form53.objects.get(pk=action_applied_to_object)
        self.action_time = Form53.objects.get(pk=action_applied_to_object).created_at

    def obj_create_action(self, action):
        ActivityLogModel.objects.create(
            action_by=self.action_by,
            action_description=FORM53_LOG_DESCRIPTIONS[action]
                               % (
                                  self.action_applied_to_object.circuit.name,
                                  self.action_applied_to_object.circuit.object.id_outfit.outfit,
                               ),
            action_time=self.action_time
        )

    def obj_delete_action(self, action):
        ActivityLogModel.objects.create(
            action_by=self.action_by,
            action_description=FORM53_LOG_DELETE_DESCRIPTIONS[action]
                               % (
                                  self.action_applied_to_object.circuit.name,
                                  self.action_applied_to_object.circuit.object.id_outfit.outfit,
                               ),
            action_time=self.action_time
        )


