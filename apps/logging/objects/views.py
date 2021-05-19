# coding: utf-8
from apps.accounts.models import Profile
from apps.logging.models import ActivityLogModel
from .constants import OBJECT_ACTIVITY_LOG_DESCRIPTIONS, TPO_ACTIVITY_LOG_DESCRIPTIONS, \
    OUTFIT_ACTIVITY_LOG_DESCRIPTIONS, POINT_ACTIVITY_LOG_DESCRIPTIONS

from apps.opu.objects.models import Object, TypeOfTrakt, TPO, AmountChannel, Outfit, Point, IP, TypeOfLocation, \
    LineType, Category, Consumer
from datetime import datetime



class ObjectActivityLogUtil:
    def __init__(self, action_by, action_applied_to_object):
        self.action_by = Profile.objects.get(user=action_by)
        self.action_applied_to_object = Object.objects.get(pk=action_applied_to_object)
        self.action_time = Object.objects.get(pk=action_applied_to_object).created_at

    def object_create_action(self, action):
        ActivityLogModel.objects.create(
            action_by=self.action_by,
            action_description=OBJECT_ACTIVITY_LOG_DESCRIPTIONS[action]
                               % (self.action_applied_to_object.name,
                                  self.action_applied_to_object.id_outfit,
                                                                    ),
            action_time=self.action_time
        )

class TPOActivityLogUtil:
    def __init__(self, action_by, action_applied_to_object):
        self.action_by = Profile.objects.get(user=action_by)
        self.action_applied_to_object = TPO.objects.get(pk=action_applied_to_object)
        self.action_time = datetime.now()

    def tpo_create_action(self, action):
        ActivityLogModel.objects.create(
            action_by=self.action_by,
            action_description=TPO_ACTIVITY_LOG_DESCRIPTIONS[action]
                               % (self.action_applied_to_object.name,
                                  self.action_applied_to_object.index,
                                  ),
            action_time=self.action_time
        )



class OutfitActivityLogUtil:
    def __init__(self, action_by, action_applied_to_object):
        self.action_by = Profile.objects.get(user=action_by)
        self.action_applied_to_object = Outfit.objects.get(pk=action_applied_to_object)
        self.action_time = Outfit.objects.get(pk=action_applied_to_object).created_at

    def obj_create_action(self, action):
        ActivityLogModel.objects.create(
            action_by=self.action_by,
            action_description=OUTFIT_ACTIVITY_LOG_DESCRIPTIONS[action]
                               % (self.action_applied_to_object.outfit,
                                  self.action_applied_to_object.adding,
                                  ),
            action_time=self.action_time
        )

class PointActivityLogUtil:
    def __init__(self, action_by, action_applied_to_object):
        self.action_by = Profile.objects.get(user=action_by)
        self.action_applied_to_object = Point.objects.get(pk=action_applied_to_object)
        self.action_time = datetime.now()

    def obj_create_action(self, action):
        ActivityLogModel.objects.create(
            action_by=self.action_by,
            action_description=POINT_ACTIVITY_LOG_DESCRIPTIONS[action]
                               % (self.action_applied_to_object.point,
                                  self.action_applied_to_object.name,
                                  ),
            action_time=self.action_time
        )




