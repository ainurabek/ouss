from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from django.db.models.fields.files import FileField
from django.utils.safestring import mark_safe
from django import template

from apps.opu.objects.models import TPO, Outfit,Point, Category, LineType, TypeOfTrakt, Object, TypeOfLocation

from apps.opu.customer.models import Customer
import os

register = template.Library()
from django.db.models import Q


def get_field_name_for_create_img(model, model_photo):
    model_fields_name = model_photo._meta.fields
    img_field = None
    obj_field = None
    for field in model_fields_name:
        if type(field) == FileField:
            img_field = str(field.name)
        if field.related_model == model:
            obj_field = str(field.name)

    return img_field, obj_field


def create_photo(model, model_photo, obj, field_name, request):
    img_field, obj_field = get_field_name_for_create_img(model, model_photo)
    for img in request.FILES.getlist(field_name):
        kwargs = {img_field: img, obj_field: obj}
        model_photo.objects.create(**kwargs)



class ListWithPKMixin:
    model = None
    serializer = None
    field_for_filter = None

    def get(self, request, pk):
        kwargs = {self.field_for_filter: pk}
        object = self.model.objects.filter(**kwargs).order_by('-id')


        serializer = self.serializer(object, many=True)


        return Response(serializer.data)


class PhotoCreateMixin:
    model = None
    model_photo = None
    search_field_for_img = None

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        create_photo(self.model, self.model_photo, obj, self.search_field_for_img, request)
        response = {"data": "Изображение успешно добавлено"}
        return Response(response, status=status.HTTP_201_CREATED)


def delete_file(file):
    if os.path.exists(file.src.path):
        os.remove(file.src.path)

class PhotoDeleteMixin:
    model_for_delete = None

    def delete(self, request, obj_pk, deleted_pk):
        photo = get_object_or_404(self.model_for_delete, pk=deleted_pk)
        if photo:
            delete_file(photo)
        photo.delete()
        response = {"data": "Изображение успешно удалено"}
        return Response(response, status=status.HTTP_204_NO_CONTENT)

@register.simple_tag
def get_object_diff(history):
    message = ''
    old_record = history.instance.history_object_log.filter(Q(history_date__lt=history.history_date)).order_by('history_date').last()
    if history and old_record:
        delta = history.diff_against(old_record)
        for change in delta.changes:
            if "tpo1"  == change.field:
                old_tpo = TPO.objects.get(pk=change.old)
                new_tpo = TPO.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old_tpo, new_tpo)
            elif "tpo2" == change.field:
                old_tpo = TPO.objects.get(pk=change.old)
                new_tpo = TPO.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old_tpo, new_tpo)
            elif "id_outfit" == change.field:
                old = Outfit.objects.get(pk=change.old)
                new = Outfit.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            elif "point1" == change.field:
                old = Point.objects.get(pk=change.old)
                new = Point.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            elif "point2" == change.field:
                old = Point.objects.get(pk=change.old)
                new = Point.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            elif "category" == change.field:
                old = Category.objects.get(pk=change.old)
                new = Category.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            elif "type_line" == change.field:
                old_type = LineType.objects.get(pk=change.old)
                new_type = LineType.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old_type, new_type)
            elif "type_of_trakt" == change.field:
                old = TypeOfTrakt.objects.get(pk=change.old)
                new = TypeOfTrakt.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            elif "customer" == change.field:
                old = Customer.objects.get(pk=change.old)
                new = Customer.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            else:
                message += "{}:{} ->-> {}".format(change.field, change.old, change.new)
        return mark_safe(message)

@register.simple_tag
def get_ip_diff(history):
    message = ''
    old_record = history.instance.history_ip_log.filter(Q(history_date__lt=history.history_date)).order_by('history_date').last()
    if history and old_record:
        delta = history.diff_against(old_record)
        for change in delta.changes:
            if "object_id"  == change.field:
                old = Object.objects.get(pk=change.old)
                new = Object.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            elif "point_id" == change.field:
                old_tpo = Point.objects.get(pk=change.old)
                new_tpo = Point.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old_tpo, new_tpo)
            elif "tpo_id" == change.field:
                old = TPO.objects.get(pk=change.old)
                new = TPO.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            else:
                message += "{}:{} ->-> {}".format(change.field, change.old, change.new)
        return mark_safe(message)

@register.simple_tag
def get_point_diff(history):
    message = ''
    old_record = history.instance.history_point_log.filter(Q(history_date__lt=history.history_date)).order_by('history_date').last()
    if history and old_record:
        delta = history.diff_against(old_record)
        for change in delta.changes:
            if "id_outfit"  == change.field:
                old = Outfit.objects.get(pk=change.old)
                new = Outfit.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            elif "tpo" == change.field:
                old = TPO.objects.get(pk=change.old)
                new = TPO.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            else:
                message += "{}:{} ->-> {}".format(change.field, change.old, change.new)
        return mark_safe(message)

@register.simple_tag
def get_outfit_diff(history):
    message = ''
    old_record = history.instance.history_outfit_log.filter(Q(history_date__lt=history.history_date)).order_by('history_date').last()
    if history and old_record:
        delta = history.diff_against(old_record)
        for change in delta.changes:
            if "type_outfit"  == change.field:
                old = TypeOfLocation.objects.get(pk=change.old)
                new = TypeOfLocation.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            elif "tpo" == change.field:
                old = TPO.objects.get(pk=change.old)
                new = TPO.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)
            else:
                message += "{}:{} ->-> {}".format(change.field, change.old, change.new)
        return mark_safe(message)