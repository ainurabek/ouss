# coding: utf-8
from django.db import models
from apps.accounts.models import Profile


class ActivityLogModel(models.Model):
    action_by = models.ForeignKey(Profile, on_delete=models.SET_NULL,
                                  blank=True, null=True)
    action_description = models.CharField(max_length=205)
    action_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Список действий'
        verbose_name_plural = 'Список действий'

    def __str__(self):
        return self.id
