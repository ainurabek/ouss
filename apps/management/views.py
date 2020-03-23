from apps.accounts.models import User, DepartmentKT
from apps.objects.models import TPO, Outfit, Point, Object
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import ObjectForm, TraktForm, TraktEditForm, ObjectFilterForm




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
    obj = Object.objects.get(pk=lp_id)
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
    return render(request, 'management/trakt.html', {'trakts': trakts, 'obj': obj, 'filter_form':filter_form})

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



