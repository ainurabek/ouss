from apps.accounts.models import User, DepartmentKT
from apps.objects.models import TPO, Outfit, Point, Object
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import ObjectForm, TraktForm, TraktEditForm, ObjectFilterForm
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
        Object.objects.filter(pk=id).update(add_time=timezone.now())

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
        Object.objects.filter(pk=id).update(add_time=timezone.now())

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

    return redirect('apps:management:trakt', lp_id=main_obj.id_parent.pk)



