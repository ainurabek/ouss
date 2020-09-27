import csv, sys, os



project_dir = "/home/ainura/Desktop/2020/KT/KT/project/"
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
import django

django.setup()

from apps.accounts.models import DepartmentKT, SubdepartmentKT, Role
from apps.opu.objects.models import TPO, Category, LineType, TypeOfLocation, Outfit, Point, InOut, TypeOfTrakt
from apps.opu.circuits.models import Measure, TypeCom, Mode
from apps.opu.form51.models import Region
from apps.opu.form_customer.models import Signalization
from apps.dispatching.models import Index, TypeOfJournal, Reason

data_tpo = csv.reader(open("/home/ainura/Desktop/DB/TPO.csv"), delimiter=',')
data_cat = csv.reader(open("/home/ainura/Desktop/DB/category.csv"), delimiter=',')
data_lin = csv.reader(open("/home/ainura/Desktop/DB/LineTypes.csv"), delimiter=',')
data_out = csv.reader(open("/home/ainura/Desktop/DB/outfits.csv"), delimiter=',')
data_loc = csv.reader(open("/home/ainura/Desktop/DB/type_location.csv"), delimiter=',')
data_point= csv.reader(open("/home/ainura/Desktop/DB/points.csv"), delimiter=',')
data_mode= csv.reader(open("/home/ainura/Desktop/DB/mode.csv"), delimiter=',')
data_department = csv.reader(open("/home/ainura/Desktop/DB/department.csv"), delimiter=',')
data_subdepartment = csv.reader(open("/home/ainura/Desktop/DB/subdepartment.csv"), delimiter=',')
data_role= csv.reader(open("/home/ainura/Desktop/DB/role.csv"), delimiter=',')
data_measure= csv.reader(open("/home/ainura/Desktop/DB/measure.csv"), delimiter=',')
data_typecom= csv.reader(open("/home/ainura/Desktop/DB/type_com.csv"), delimiter=',')
data_region= csv.reader(open("/home/ainura/Desktop/DB/region.csv"), delimiter=',')
data_signal= csv.reader(open("/home/ainura/Desktop/DB/signalization.csv"), delimiter=',')
data_inout= csv.reader(open("/home/ainura/Desktop/DB/inout.csv"), delimiter=',')
data_trakt= csv.reader(open("/home/ainura/Desktop/DB/type_trakt.csv"), delimiter=',')
data_index= csv.reader(open("/home/ainura/Desktop/DB/index.csv"), delimiter=',')
data_typejournal= csv.reader(open("/home/ainura/Desktop/DB/type_journal.csv"), delimiter=',')
data_reason= csv.reader(open("/home/ainura/Desktop/DB/reason.csv"), delimiter=',')



for row in data_tpo:
    if row[0] != 'id':
        tpo = TPO()
        tpo.name = row[1]
        tpo.index = row[2]
        tpo.save()

for row in data_index:
    if row[0] != 'id':
        index = Index()
        index.index = row[1]
        index.name = row[2]
        index.save()


for row in data_typejournal:
    if row[0] != 'id':
        jour = TypeOfJournal()
        jour.name = row[1]
        jour.save()

for row in data_reason:
    if row[0] != 'id':
        r = Reason()
        r.name = row[1]
        r.save()


for row in data_signal:
    if row[0] != 'id':
        sig = Signalization()
        sig.name = row[1]
        sig.save()

for row in data_inout:
    if row[0] != 'id':
        out = InOut()
        out.name = row[1]
        out.save()

for row in data_trakt:
    if row[0] != 'id':
        trakt = TypeOfTrakt()
        trakt.name = row[1]
        trakt.save()


for row in data_region:
    if row[0] != 'id':
        region = Region()
        region.name = row[1]
        region.slug = row[2]
        region.save()


for row in data_department:
    if row[0] != 'id':
        dep = DepartmentKT()
        dep.name = row[1]
        dep.save()

for row in data_typecom:
    if row[0] != 'id':
        type_com = TypeCom()
        type_com.name = row[1]
        type_com.save()

for row in data_measure:
    if row[0] != 'id':
        mes = Measure()
        mes.name = row[1]
        mes.save()
for row in data_role:
    if row[0] != 'id':
        role = Role()
        role.name = row[1]
        role.save()
for row in data_subdepartment:
    if row[0] != 'id':
        subdep = SubdepartmentKT()
        subdep.department_id = row[1]
        subdep.name = row[2]
        subdep.save()

for row in data_cat:
  if row[0] != 'index':
    post = Category()
    post.index = row[0]
    post.name = row[1]
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

for row in data_out:
  if row[0] != 'id':
    post = Outfit()
    # post.id = row[0]
    post.outfit = row[1]
    post.adding = row[2]
    post.num_outfit = row[3]
    post.tpo_id = row[6]
    post.type_outfit_id = row[7]
    # post.created_by_id = row[6]
    # post.created_at = row[7]
    post.save()

for row in data_point:
  if row[0] != 'id':
    print(row[0])
    post = Point()
    # post.id = row[0]
    post.point = row[1]
    post.name = row[2]
    post.id_outfit_id = row[3]
    post.tpo_id = row[4]
    post.save()