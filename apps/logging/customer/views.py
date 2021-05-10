# coding: utf-8
from apps.accounts.models import Profile
from apps.logging.models import ActivityLogModel
from .constants import CUSTOMER_LOG_DESCRIPTIONS
from apps.opu.customer.models import Customer
from datetime import datetime



class CustomerLogUtil:
    def __init__(self, action_by, action_applied_to_object):
        self.action_by = Profile.objects.get(user=action_by)
        self.action_applied_to_object = Customer.objects.get(pk=action_applied_to_object)
        self.action_time = datetime.now()

    def obj_create_action(self, action):
        ActivityLogModel.objects.create(
            action_by=self.action_by,
            action_description=CUSTOMER_LOG_DESCRIPTIONS[action]
                               % (
                                  self.action_applied_to_object.object.name,
                                  self.action_applied_to_object.customer.abr,
                                  ),
            action_time=self.action_time
        )

