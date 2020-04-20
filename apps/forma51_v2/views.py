from django.shortcuts import render, get_object_or_404, redirect
from apps.form51.models import Region
from apps.forma51_v2.models import Forma
from apps.forma51_v2.forms import Forma51Form
from apps.objects.models import Object

def region_list(request):
	regions = Region.objects.all()
	return render(request, 'management/list_region.html', {'regions': regions})

def form51_list(request, slug):
	region = get_object_or_404(Region, slug=slug)
	objects = Forma.objects.filter(region=region)
	return render(request, 'management/form51_list.html', {'objects': objects})

def create_form51(request, pk):
	obj = get_object_or_404(Object, pk=pk)
	region = None
	if request.method == 'POST':
		form = Forma51Form(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.object = obj
			region = post.region.slug
			post.save()
			return redirect('apps:forma51_v2:form51_list', slug=region)
	else:
		form = Forma51Form()
	return render(request, 'management/create_form51.html', {'form': form})



