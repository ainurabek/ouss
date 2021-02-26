import csv, sys, os



project_dir = "/home/ainura/Desktop/2020/KT/KT/project/"
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
import django

django.setup()

from apps.opu.objects.models import  Object


#добавить все задействованные каналы к ипам обьектов
# all_pg = Object.objects.filter(type_of_trakt__name='ПГ')
# kls = all_pg.filter(type_line__main_line_type__name="КЛС")
# kls_point1 = kls.distinct('point1').order_by('point1')
# kls_point2 = kls.distinct('point2').order_by('point2')
# kls_points = [*kls_point1, *kls_point2]
#
# for point in kls_points:
#     count_1 = 0
#     for channel in kls.filter(point1=point.point1):
#         count_1 += channel.total_amount_channels
#     point.point1.total_point_channels_KLS  = count_1
#     point.point1.save()
#     count_2 = 0
#     for channel in kls.filter(point2=point.point2):
#         count_2 += channel.total_amount_channels
#     point.point2.total_point_channels_KLS = count_2
#     point.point2.save()
#
# rrl = all_pg.filter(type_line__main_line_type__name="ЦРРЛ")
# rrl_point1 = rrl.distinct('point1').order_by('point1')
# rrl_point2 = rrl.distinct('point2').order_by('point2')
#
# rrl_points = [*rrl_point1, *rrl_point2]
#
# for point in rrl_points:
#     count_1 = 0
#     for channel in rrl.filter(point1=point.point1):
#         count_1 += channel.total_amount_channels
#     point.point1.total_point_channels_RRL  = count_1
#     point.point1.save()
#     count_2 = 0
#     for channel in rrl.filter(point2=point.point2):
#         count_2 += channel.total_amount_channels
#     point.point2.total_point_channels_RRL = count_2
#     point.point2.save()

all_objs = Object.objects.all()
for obj in all_objs:
    obj.reserve_transit.clear()
    obj.reserve_transit2.clear()

