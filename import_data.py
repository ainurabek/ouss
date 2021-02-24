import csv, sys, os

project_dir = "/code/project/"
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
import django

django.setup()

from apps.opu.objects.models import TPO, TypeOfLocation, Outfit, Point

data_tpo = csv.reader(open("/code/folder/ТПО.csv"), delimiter=',')
data_out = csv.reader(open("/code/folder/Предприятия.csv"), delimiter=',')
data_loc = csv.reader(open("/code/folder/type_location.csv"), delimiter=',')
data_point= csv.reader(open("/code/folder/points.csv"), delimiter=',')

for row in data_tpo:
    if row[0] != 'id':
        tpo = TPO()
        tpo.name = row[1]
        tpo.index = row[2]
        tpo.save()

for row in data_loc:
  if row[0] != 'id':
    post = TypeOfLocation()
    post.name = row[1]
    post.save()

for row in data_out:
  if row[0] != 'id':
    post = Outfit()
    post.outfit = row[1]
    post.adding = row[2]
    post.num_outfit = row[3]
    post.tpo_id = row[6]
    post.type_outfit_id = row[7]
    post.save()

for row in data_point:
  if row[0] != 'id':
    print(row[0])
    post = Point()
    post.point = row[1]
    post.name = row[2]
    post.id_outfit_id = row[3]
    post.tpo_id = row[4]
    post.save()
