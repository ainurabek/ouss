from apps.opu.services import get_field_name_for_create_img


def create_photo_for_form53(model, model_photo, obj, field_name: str, request):
    img_field, obj_field = get_field_name_for_create_img(model, model_photo)
    for img in request.FILES.getlist(field_name):
        kwargs = {img_field: img}
        obj_photo = model_photo.objects.create(**kwargs)
        obj_photo.form53.add(obj)
