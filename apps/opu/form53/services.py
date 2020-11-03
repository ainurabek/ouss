from apps.opu.services import get_field_name_for_create_img
from django.utils.safestring import mark_safe
from django import template

from apps.opu.circuits.models import Circuit

register = template.Library()
from django.db.models import Q

def create_photo_for_form53(model, model_photo, obj, field_name: str, request):
    img_field, obj_field = get_field_name_for_create_img(model, model_photo)
    for img in request.FILES.getlist(field_name):
        kwargs = {img_field: img}
        obj_photo = model_photo.objects.create(**kwargs)
        obj_photo.form53.add(obj)

@register.simple_tag
def get_form53_diff(history):
    message = ''
    old_record = history.instance.history_form53_log.filter(Q(history_date__lt=history.history_date)).order_by('history_date').last()
    if history and old_record:
        delta = history.diff_against(old_record)
        for change in delta.changes:
            if "circuit"  == change.field:
                old = Circuit.objects.get(pk=change.old)
                new = Circuit.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old, new)

            else:
                message += "{}:{} ->-> {}".format(change.field, change.old, change.new)
        return mark_safe(message)
