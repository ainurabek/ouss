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

class CreateMixinWithPhoto:
    model = None
    model_photo = None
    serializer = None
    search_fields_for_img = None

    def get_field_name(self):
        model_fields_name = self.model._meta.fields
        obj_field = None
        for field in model_fields_name:
            if field.related_model == self.model:
                obj_field = str(field.name)
                break
        return obj_field


    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=obj.customer, created_by=request.user.profile)
            obj_kwargs = {self.get_field_name(): obj}
            serializer.save(**obj_kwargs)
            img_field, obj_field = get_field_name_for_create_img(serializer, self.model_photo)

            for field in self.search_fields_for_img:
                for img in request.FILES.getlist(field):
                    kwargs = {img_field: img, obj_field: serializer}
                    self.model_photo.objects.create(**kwargs)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListWithPKMixin:
    model = None
    serializer = None
    field_for_filter = None

    def get(self, request, pk):
        kwargs = {self.field_for_filter: pk}
        object = self.model.objects.filter(**kwargs)
        serializer = self.serializer(object, many=True)
        return Response(serializer.data)


class PhotoCreateMixin:
    model = None
    model_photo = None
    search_fields_for_img = None
    add = False

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        img_field, obj_field = get_field_name_for_create_img(self.model, self.model_photo)
        for field in self.search_fields_for_img:
            for img in request.FILES.getlist(field):
                kwargs = {img_field: img, obj_field: obj}
                self.model_photo.objects.create(**kwargs)

        return Response(status=status.HTTP_201_CREATED)



class PhotoDeleteMixin:
    model_for_delete = None

    def delete(self, request, obj_pk, deleted_pk):
        get_object_or_404(self.model_for_delete, pk=deleted_pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)