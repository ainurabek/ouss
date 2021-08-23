import csv, sys, os



project_dir = "/home/ainura/Desktop/2020/KT/KT/project/"
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
import django

django.setup()
from apps.accounts.models import User
from apps.opu.objects.models import Object, Transit, Bridge, Point, Outfit
from apps.opu.circuits.service import create_circuit_transit
# from apps.analysis.models import AmountChannelsKLSRRL
from apps.dispatching.models import Event
from apps.secondary.models import TypeStation, SecondaryBase, AmbulanceNumsBase

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

# all_objs = Object.objects.all()
# for obj in all_objs:
#     obj.reserve_transit.clear()
#     obj.reserve_transit2.clear()

# main_events = Event.objects.filter(callsorevent = True)
# for event in main_events:
#     last = event.event_id_parent.all().order_by('-date_from')[0]
#     event.created_at = last.created_at
#     event.save()

# events = Event.objects.filter(callsorevent = True)
# for event in events:
#
#     calls  = event.event_id_parent.all()
#     for call in calls:
#         call.object = event.object
#         call.ips = event.ips
#         call.circuit = event.circuit
#         call.save()

# objects = Object.objects.all()
# for obj in objects:
#     AmountChannelsKLSRRL.objects.create(object = obj)
# points = Point.objects.all()
# for point in points:
#     AmountChannelsKLSRRL.objects.create(ips=point)

# all_events = Event.objects.all()
# for event in all_events:
#     all_calls = event.event_id_parent.all().order_by('-date_from')
#     i = 0
#     while i < (len(all_calls)-1):
#         all_calls[i + 1].date_to = all_calls[i].date_from
#         all_calls[i + 1].save()
#         i += 1
#     all_calls[0].date_to = None
#     all_calls[0].save()
#     all_calls[i].id_parent.date_from = all_calls.last().date_from
#     if len(all_calls) == 1:
#         all_calls[i].id_parent.date_to = None
#     else:
#         all_calls[i].id_parent.date_to = all_calls[0].date_from
#     all_calls[i].id_parent.index1 = all_calls[0].index1
#     all_calls[i].id_parent.created_at = all_calls[0].created_at
#     all_calls[i].id_parent.responsible_outfit = all_calls[0].responsible_outfit
#     all_calls[i].id_parent.save()

# unique_trassa = []
# reserve_trassa = []
#
# for obj in Object.objects.all():
#     trassa = [*obj.transit.all()[::-1], *obj.transit2.all()]
#     res_trassa = [*obj.reserve_transit.all()[::-1], *obj.reserve_transit2.all()]
#
#     if len(trassa) > 1 and trassa not in unique_trassa:
#         unique_trassa.append(trassa)
#     if len(res_trassa) > 1 and res_trassa not in reserve_trassa:
#         reserve_trassa.append(res_trassa)
#
#
# for trassa in unique_trassa:
#     tr = Transit.objects.create(name="Основная трасса", create_circuit_transit=True)
#     for obj in trassa:
#         tr.trassa.add(obj)
#         Bridge.objects.create(object=obj, transit=tr)
#     create_circuit_transit(tr)
#
#
# for trassa in reserve_trassa:
#     tr = Transit.objects.create(name="Резерв", create_circuit_transit=False)
#     for obj in trassa:
#         tr.trassa.add(obj)
#         Bridge.objects.create(object=obj, transit=tr)

data_type_station = csv.reader(open("/code/db/type_station.csv"), delimiter=',')
data_ambul = csv.reader(open("/code/db/ambul.csv"), delimiter=',')
data_second = csv.reader(open("/home/ainura/Desktop/DB/vtorichka.csv"), delimiter=',')

# for index, row in enumerate(data_second):
#     try:
#         Point.objects.get(point=row[1])
#     except Point.DoesNotExist:
#         print(row[0])

for row in data_type_station:
    if row[0] != 'id':
        type_station = TypeStation()
        type_station.name = row[1]
        type_station.save()

# for row in data_ambul:
#     if row[0] != 'id':
#         ambul = AmbulanceNumsBase()
#         ambul.outfit = Outfit.objects.get(id=row[1])
#         ambul.region = row[2]
#         ambul.code = row[3]
#         ambul.main_num = row[4]
#         ambul.first_redirection=row[5]
#         ambul.second_redirection = row[6]
#         ambul.third_redirection = row[7]
#         ambul.comments = row[8]
#         ambul.save()

# for row in data_second:
#     if row[0] != 'id':
#         second = SecondaryBase()
#         second.point = Point.objects.get(point=row[1])
#         second.type_station = TypeStation.objects.get(name=row[2])
#         second.administrative_division = row[3]
#         second.year_of_launch = row[4]
#         outfit = Outfit.objects.get(id=row[5])
#         second.outfit = outfit
#         second.free_numbering = row[6]
#         second.installed_value = row[7]
#         second.active_value = row[8]
#         second.active_numbering=row[9]
#         second.KT_numbering=row[10]
#         second.GAS_numbering = row[11]
#         second.GAS_return=row[12]
#         second.comments=row[13]
#         second.created_by=User.objects.get(id=row[14])
#         second.save()