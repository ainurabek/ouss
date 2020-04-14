from apps.accounts.models import User, DepartmentKT
from apps.objects.models import TPO, Outfit, Point, Object, Trassa

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import ObjectForm, TraktForm, TraktEditForm, ObjectFilterForm, Form51Form, Form51FilterForm
from django.db.models import Q
from django.utils import timezone




# def management_index(request):
#     users = User.objects.all()
#     departments = DepartmentKT.objects.all()
#     lps = Object.objects.filter(id_parent=None)
#     return render(request, 'management/index.html', {
#         'users': users,
#         'departments':departments,
#         'lps': lps
#     })
from ..form51.models import Region, Form51


def tpo_list(request):
    tpos = TPO.objects.all()

    return render(request, 'management/tpo.html', {
        'tpos': tpos

    })

def outfit_list(request):
    outfits = Outfit.objects.all()

    return render(request, 'management/outfit.html', {
        'outfits': outfits

    })

def point_list(request):
    points = Point.objects.all()
    return render(request, 'management/point.html', {
        'points': points

    })

def base(request):
    lps = Object.objects.filter(id_parent=None)
    context = {
        'lps': lps
    }
    return render(request, 'management/base.html', context)

def lp_list(request):
    lps = Object.objects.filter(id_parent=None)
    filter_form = ObjectFilterForm(request.GET or None)
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('name'):
            lps = lps.filter(
                name=filter_form.cleaned_data.get('name')
            )
        if filter_form.cleaned_data.get('id_outfit'):
            lps = lps.filter(
                id_outfit=filter_form.cleaned_data.get('id_outfit')
            )
        if filter_form.cleaned_data.get('tpo1'):
            lps = lps.filter(
                tpo1=filter_form.cleaned_data.get('tpo1')
            )
        if filter_form.cleaned_data.get('point1'):
            lps = lps.filter(
                point1=filter_form.cleaned_data.get('point1')
            )
        if filter_form.cleaned_data.get('tpo2'):
            lps = lps.filter(
                tpo2=filter_form.cleaned_data.get('tpo2')
            )
        if filter_form.cleaned_data.get('point2'):
            lps = lps.filter(
                point2=filter_form.cleaned_data.get('point2')
            )
        if filter_form.cleaned_data.get('type_line'):
            lps = lps.filter(
                type_line=filter_form.cleaned_data.get('type_line')
            )

    context = {
        'lps': lps,
        'filter_form': filter_form,
    }
    return render(request, 'management/index.html', context)

def lp_create(request):
    form = ObjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('apps:management:lp')
    return render(request, 'management/lp_form.html', {'form': form})

def lp_edit(request, pk):
    lp = get_object_or_404(Object, pk=pk)
    if request.method == "POST":
        form = ObjectForm(request.POST, request.FILES,  instance=lp)
        if form.is_valid():
            lp.save()
            return redirect('apps:management:lp')
    else:
        form = ObjectForm(instance=lp)
    return render(request, 'management/lp_form.html', {'form': form})

def lp_delete(request, pk=None):
    if pk:
        lp = Object.objects.get(id=pk)
        lp.delete()
        return redirect('apps:management:lp')

def trakt_list(request, lp_id):
    parent = Object.objects.get(pk=lp_id)
    trakts= Object.objects.filter(id_parent=lp_id)
    filter_form = ObjectFilterForm(request.GET or None)
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('name'):
            trakts = trakts.filter(
                name=filter_form.cleaned_data.get('name')
            )
        if filter_form.cleaned_data.get('id_outfit'):
            trakts = trakts.filter(
                id_outfit=filter_form.cleaned_data.get('id_outfit')
            )
        if filter_form.cleaned_data.get('tpo1'):
            trakts = trakts.filter(
                tpo1=filter_form.cleaned_data.get('tpo1')
            )
        if filter_form.cleaned_data.get('point1'):
            trakts = trakts.filter(
                point1=filter_form.cleaned_data.get('point1')
            )
        if filter_form.cleaned_data.get('tpo2'):
            trakts = trakts.filter(
                tpo2=filter_form.cleaned_data.get('tpo2')
            )
        if filter_form.cleaned_data.get('point2'):
            trakts = trakts.filter(
                point2=filter_form.cleaned_data.get('point2')
            )

        if filter_form.cleaned_data.get('amount_channels'):
            trakts = trakts.filter(
                amount_channels=filter_form.cleaned_data.get('amount_channels')
            )

    if int(trakts.count()) > 0:
        obj = trakts[0]
        context = {
            'trakts': trakts, 
            'obj': obj, 
            'filter_form':filter_form,
            'parent': parent
            }
    else:
        context = {
            'trakts': trakts, 
            'parent': parent, 
            'filter_form':filter_form           
        }
    return render(request, 'management/trakt.html', context)

def trakt_create(request, lp_id):
    lp = get_object_or_404(Object, id=lp_id)
    form = TraktForm(request.POST or None, request.FILES or None, id_parent=lp_id)
    if form.is_valid():
        trakt = form.save(commit=False)
        trakt.id_parent = lp
        trakt.save()
        return redirect('apps:management:trakt', lp_id=lp_id)
    return render(request, 'management/trakt_form.html', {'form': form})


def trakt_edit(request, pk):
    trakt = get_object_or_404(Object, id=pk)
    if request.method == "POST":
        form = TraktEditForm(request.POST, instance=trakt)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            return redirect('apps:management:trakt', lp_id=trakt.id_parent.id)
    else:
        form=TraktEditForm(instance=trakt)
    return render(request, 'management/trakt_form.html', {'form': form})

def trakt_delete(request, pk):
    if pk:
        trakt = Object.objects.get(id=pk)
        trakt.delete()
        return redirect('apps:management:trakt', lp_id=trakt.id_parent.pk)


def select_obj(request, pk):
    obj = Object.objects.get(pk=pk)
    ip_ot = Object.objects.filter(Q(point1=obj.point1) | Q(point2=obj.point1))
    ip_do = Object.objects.filter(Q(point1=obj.point2) | Q(point2=obj.point2))


    trassa_list1 = obj.transit.all().order_by('-add_time')
    trassa_list2 = obj.transit2.all().order_by('add_time')

    context = {
        'obj': obj,
        'trassa_list1': trassa_list1,
        'trassa_list2': trassa_list2,
        'ip_ot': ip_ot,
        'ip_do': ip_do
    }


    return render(request, 'management/select_obj.html', context)


def left_trassa(request, pk, id):
    user = request.user.profile
    main_obj = Object.objects.get(pk=pk)
    obj = Object.objects.get(pk=id)

    ip_ot = Object.objects.filter(Q(point1=obj.point1) | Q(point2=obj.point1))
    ip_do = Object.objects.filter(Q(point1=obj.point2) | Q(point2=obj.point2))

    if main_obj.transit.filter(pk=id).exists():
        main_obj.transit.remove(obj)
        obj.transit2.clear()
        obj.transit.clear()
    else:
        main_obj.transit.add(obj)
        Object.objects.filter(pk=id).update(add_time=timezone.now(), maker_trassa=user)

    trassa_list1 = main_obj.transit.all().order_by('-add_time')
    trassa_list2 = main_obj.transit2.all().order_by('add_time')

    context = {
        'obj': main_obj,
        'trassa_list1': trassa_list1,
        'trassa_list2': trassa_list2,
        'ip_ot': ip_ot,
        'ip_do': ip_do
    }
    return render(request, 'management/trassa.html', context)


def right_trassa(request, pk, id):
    user = request.user.profile
    main_obj = Object.objects.get(pk=pk)
    obj = Object.objects.get(pk=id) 

    ip_ot = Object.objects.filter(Q(point1=obj.point1) | Q(point2=obj.point1))
    ip_do = Object.objects.filter(Q(point1=obj.point2) | Q(point2=obj.point2))

    if main_obj.transit2.filter(pk=id).exists():
        main_obj.transit2.remove(obj)
        obj.transit2.clear()
        obj.transit.clear()
    else:
        main_obj.transit2.add(obj)
        Object.objects.filter(pk=id).update(add_time=timezone.now(), maker_trassa=user)

    trassa_list1 = main_obj.transit.all().order_by('-add_time')
    trassa_list2 = main_obj.transit2.all().order_by('add_time')

    context = {
        'obj': main_obj,
        'trassa_list1': trassa_list1,
        'trassa_list2': trassa_list2,
        'ip_ot': ip_ot,
        'ip_do': ip_do
    }   

    return render(request, 'management/trassa.html', context)


def save_trassa(request, pk):
    user = request.user.profile
    main_obj = Object.objects.get(pk=pk)

    for i in main_obj.transit.all():
        if main_obj.transit.all() not in i.transit.all():
            i.transit.add(*main_obj.transit.all())

        if main_obj.transit2.all() not in i.transit2.all():
            i.transit2.add(*main_obj.transit2.all())

    for i in main_obj.transit2.all():
        if main_obj.transit2.all() not in i.transit2.all():
            i.transit2.add(*main_obj.transit2.all())
        if main_obj.transit.all() not in i.transit.all():
           i.transit.add(*main_obj.transit.all())

    trassa_list1 = main_obj.transit.all().order_by('-add_time')
    trassa_list2 = main_obj.transit2.all().order_by('add_time')

    items1 = []
    for name in trassa_list1:
        trassa = {}
        trassa['point1'] = name.point1.point
        trassa['name'] = name.name
        trassa['point2'] = name.point2.point
        items1.append(trassa)
    point1 = [item['point1'] for item in items1]
    name = [item['name'] for item in items1]
    point2 = [item['point2'] for item in items1]
    items1_trassa = point1 + name + point2
    fin_trassa1 = (' '.join(str(x) for x in items1_trassa))

    items2 = []
    for name in trassa_list2:
        trassa = {}
        trassa['point1'] = name.point1.point
        trassa['name'] = name.name
        trassa['point2'] = name.point2.point
        items2.append(trassa)
    point1 = [item['point1'] for item in items2]
    name = [item['name'] for item in items2]
    point2 = [item['point2'] for item in items2]
    items2_trassa = point1 + name + point2
    fin_trassa2 = (' '.join(str(x) for x in items2_trassa))
    name = '(' + fin_trassa1 + ')' + '(' + fin_trassa2 + ')'
    trassa_saved = Trassa.objects.create(name=name, created_by=user)
    trassa_saved.save()

    return redirect('apps:management:trassa_list')


def trassa_list(request):
    trassa_list = Object.objects.exclude(transit=None, transit2=None)
    _list = []
    for i in trassa_list:
        _list.append({'name': i.name, 
            'transit': i.transit.order_by('-add_time'), 
            'transit2': i.transit2.order_by('add_time'),
            'maker_trassa': i.maker_trassa,
            'add_time': i.add_time,
            'id': i.pk})

    return render(request, 'management/trassa_list.html', {'trassa_list': _list})


def region_list(request):
    return render(request, 'management/region_list.html', {
        'regions': Region.objects.all()
    })

def form51_list(request, slug):
    region = get_object_or_404(Region, slug=slug)
    forms = Form51.objects.filter(region=region)
    filter_form = Form51FilterForm(request.GET or None)
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('trassa', None):
            forms = forms.filter(trassa=filter_form.cleaned_data.get('trassa'))
        if filter_form.cleaned_data.get('num', None):
            forms = forms.filter(
                num=filter_form.cleaned_data.get('num')
            )
        if filter_form.cleaned_data.get('direction', None):
            forms = forms.filter(
                direction=filter_form.cleaned_data.get('direction')
            )
        if filter_form.cleaned_data.get('customer', None):
            forms = forms.filter(
                customer=filter_form.cleaned_data.get('customer')
            )
        if filter_form.cleaned_data.get('object', None):
            forms = forms.filter(
                object=filter_form.cleaned_data.get('object')
            )
        if filter_form.cleaned_data.get('amount_inst_channels', None):
            forms = forms.filter(
                amount_inst_channels=filter_form.cleaned_data.get('amount_inst_channels')
            )

        if filter_form.cleaned_data.get('amount_inv_channels', None):
            forms = forms.filter(
                amount_inv_channels=filter_form.cleaned_data.get('amount_inv_channels')
            )
        if filter_form.cleaned_data.get('reserve', None):
            forms = forms.filter(
                reserve=filter_form.cleaned_data.get('reserve')
            )
    return render(request, 'management/form51.html', {
        'region': region,
        'forms': forms,
        'filter_form':filter_form
    })

def form51_create(request, slug):
    region = get_object_or_404(Region, slug=slug)
    form = Form51Form(request.POST or None)
    if form.is_valid():
        form51=form.save(commit=False)
        form51.region=region
        form51.save()

        return redirect('apps:management:form51', slug=slug)
    return render(request, 'management/form51_create.html', {'form': form,
                                                             'region':region})

def form51_edit(request, slug, pk):
    region = Region.objects.get(slug=slug)
    if pk:
        form51 = Form51.objects.get(id=pk)
        form = Form51Form(request.POST or None, instance=form51)
        if request.method == 'POST':
            form = Form51Form(request.POST or None, instance=form51)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.region = region
                instance.save()
                return redirect('apps:management:form51', slug=slug)
        return render(request, 'management/form51_create.html', {'form': form})

def form51_delete(request, pk):
    if pk:
        form51 = Form51.objects.get(id=pk)
        form51.delete()
        return redirect('apps:management:form51', slug=form51.region.slug)