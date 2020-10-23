from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from django.db.models.fields.files import ImageField


def get_field_name_for_create_img(model, model_photo):
    model_fields_name = model_photo._meta.fields
    img_field = None
    obj_field = None
    for field in model_fields_name:
        if type(field) == ImageField:
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


class PhotoDeleteMixin:
    model_for_delete = None

    def delete(self, request, obj_pk, deleted_pk):
        get_object_or_404(self.model_for_delete, pk=deleted_pk).delete()
        response = {"data": "Изображение успешно удалено"}
        return Response(response, status=status.HTTP_204_NO_CONTENT)