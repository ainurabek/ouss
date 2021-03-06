# coding: utf-8
from apps.accounts.models import Profile
from apps.logging.models import ActivityLogModel
from .constants import FORM_CUSTOMER_CIRCUIT_LOG_DESCRIPTIONS, \
    FORM_CUSTOMER_OBJECT_LOG_DESCRIPTIONS, FORM_CUSTOMER_CIRCUIT_DELETE_LOG_DESCRIPTIONS, \
    FORM_CUSTOMER_OBJECT_DELETE_LOG_DESCRIPTIONS
from apps.opu.form_customer.models import Signalization, Form_Customer
from datetime import datetime




class FormCustomerCircuitLogUtil:
    def __init__(self, action_by, action_applied_to_object):
        self.action_by = Profile.objects.get(user=action_by)
        self.action_applied_to_object = Form_Customer.objects.get(pk=action_applied_to_object).circuit
        self.action_time = Form_Customer.objects.get(pk=action_applied_to_object).created_at

    def obj_create_action(self, action):
        ActivityLogModel.objects.create(
            action_by=self.action_by,
            action_description=FORM_CUSTOMER_CIRCUIT_LOG_DESCRIPTIONS[action]
                               % (
                                  self.action_applied_to_object.name,
                                  ),
            action_time=self.action_time
        )
    def obj_delete_action(self, action):
        ActivityLogModel.objects.create(
            action_by=self.action_by,
            action_description=FORM_CUSTOMER_CIRCUIT_DELETE_LOG_DESCRIPTIONS[action]
                               % (
                                  self.action_applied_to_object.name,
                                  ),
            action_time=self.action_time
        )
class FormCustomerObjectLogUtil:
    def __init__(self, action_by, action_applied_to_object):
        self.action_by = Profile.objects.get(user=action_by)
        self.action_applied_to_object = Form_Customer.objects.get(pk=action_applied_to_object).object
        self.action_time = Form_Customer.objects.get(pk=action_applied_to_object).created_at

    def obj_create_action(self, action):
        ActivityLogModel.objects.create(
            action_by=self.action_by,
            action_description=FORM_CUSTOMER_OBJECT_LOG_DESCRIPTIONS[action]
                               % (
                                  self.action_applied_to_object.name,
                                  ),
            action_time=self.action_time
        )

    def obj_delete_action(self, action):
        ActivityLogModel.objects.create(
            action_by=self.action_by,
            action_description=FORM_CUSTOMER_OBJECT_DELETE_LOG_DESCRIPTIONS[action]
                               % (
                                  self.action_applied_to_object.name,
                                  ),
            action_time=self.action_time
        )

