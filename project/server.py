import csv, sys, os

project_dir = "/home/ainura/Desktop/2020/KT/KT/project/"
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
import django

django.setup()
from apps.accounts.models import Role, DepartmentKT, SubdepartmentKT
from apps.opu.objects.models import Category, LineType, TypeOfLocation, TypeOfTrakt
from apps.opu.circuits.models import Mode

data_role = csv.reader(open("/home/ainura/Desktop/DB/role.csv"), delimiter=',')
data_cat = csv.reader(open("/home/ainura/Desktop/DB/category.csv"), delimiter=',')
data_lin = csv.reader(open("/home/ainura/Desktop/DB/LineTypes.csv"), delimiter=',')
data_dep = csv.reader(open("/home/ainura/Desktop/DB/department.csv"), delimiter=',')
data_loc = csv.reader(open("/home/ainura/Desktop/DB/type_location.csv"), delimiter=',')
data_subdep= csv.reader(open("/home/ainura/Desktop/DB/subdepartment.csv"), delimiter=',')
data_mode= csv.reader(open("/home/ainura/Desktop/DB/mode.csv"), delimiter=',')
data_trakt= csv.reader(open("/home/ainura/Desktop/DB/type_trakt.csv"), delimiter=',')


for row in data_role:
    if row[0] != 'id':
        role = Role()
        role.name = row[1]
        role.save()

for row in data_cat:
  if row[0] != 'index':
    post = Category()
    post.index = row[1]
    post.name = row[2]
    post.save()

for row in data_lin:
  if row[0] != 'id':
    post = LineType()
    # post.id = row[0]
    post.name = row[1]
    post.save()

for row in data_loc:
  if row[0] != 'id':
    post = TypeOfLocation()
    # post.id = row[0]
    post.name = row[1]
    post.save()

for row in data_mode:
  if row[0] != 'id':
    post = Mode()
    # post.id = row[0]
    post.name = row[1]
    post.save()

for row in data_dep :
  if row[0] != 'id':
    post = DepartmentKT()
    # post.id = row[0]
    post.name = row[1]
    post.save()

for row in data_subdep:
  if row[0] != 'id':
    print(row[0])
    post = SubdepartmentKT()
    # post.id = row[0]
    post.department = row[1]
    post.name = row[2]
    post.save()

for row in data_trakt:
  if row[0] != 'id':
    print(row[0])
    post = TypeOfTrakt()
    # post.id = row[0]
    post.name = row[1]
    post.save()