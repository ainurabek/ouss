import datetime

now = datetime.datetime.now()


from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.urls import reverse_lazy

from .forms import ShutdownFilterForm, RequestForm
from .models import Request, ShutdownLog, Status
from django.http import HttpResponse, HttpResponseRedirect


class StatementCreateView(CreateView):
    """Создания заявки"""
    model = Request
    template_name = 'dispatching/statement_create.html'
    success_url = '/'
    fields = ['type_request', 'address', 'first_name',
              'type_of_applicant', 'status', 'last_name',
              'home_phone', 'telephone_number', 'date_from',
              'date_to', 'department', 'description']

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        return super().form_valid(form)


class ShutdownCreateView(CreateView):
    """Создания отключения"""
    model = ShutdownLog
    fields = ['shutdown_type', 'address','region',
              'status', 'shutdown_periods_from',
              'shutdown_periods_to', 'сause']

    template_name = 'dispatching/shutdown_create.html'
    success_url = reverse_lazy('apps:dispatching:shutdown_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        return super().form_valid(form)


class RequestList(ListView):
    """Список заявок"""
    model = Request
    template_name = 'dispatching/request_list.html'
    context_object_name = 'request_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        status_list = Status.objects.all()
        context = {'status_list': status_list}
        return super().get_context_data(**context)


def list_of_filtered(request, pk):
    """Список отфильтрованных заявок"""
    requests = Request.objects.filter(status=pk)
    status_list = Status.objects.all()
    return render(request, 'dispatching/request_list.html', {'request_list': requests, 'status_list': status_list})


def status_list(request):
    news = Request.objects.filter(status__id=1)
    return render(request, 'dispatching/status_list.html', {'news': news})

# class RequestCreateView(CreateView):
#     """Создания отключения"""
#     model = Request
#     fields = ['first_name', 'last_name', 'address', 'status', 'type_request',
#               'description', 'created_by']
#
#     template_name = 'dispatching/request_create.html'
#     success_url = reverse_lazy('apps:dispatching:request_list')
#
#     def form_valid(self, form):
#         print(self.request.user.profile)
#         form.instance.created_by = self.request.user.profile
#         print(self.request.user.profile)
#         return super().form_valid(form)


def request_create(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user.profile
            post.created_at = datetime.datetime.now()
            post.save()
            return redirect('apps:dispatching:request_list')
    else:
        form = RequestForm()
    return render(request, 'dispatching/request_create.html', {'form': form})


def request_edit(request, request_id):
    request1 = get_object_or_404(Request, pk=request_id)
    if request.method == "POST":
        form = RequestForm(request.POST, instance=request1)
        if form.is_valid():
            request1 = form.save(commit=False)
            request1.created_by = request.user.profile
            request1.created_at = datetime.datetime.now()
            request1.save()
            return redirect('apps:dispatching:request_list')
    else:
        form = RequestForm(instance=request1)
    return render(request, 'dispatching/request_create.html', {'form': form})


def request_delete(request, pk):
    Request.objects.get(pk=pk).delete()
    return redirect('apps:dispatching:request_list')


def shutdown_list(request):
    """Список отключений"""
    objs = ShutdownLog.objects.all()
    filter_form = ShutdownFilterForm(request.GET or None)
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('shutdown_type'):
            objs = objs.filter(
                shutdown_type=filter_form.cleaned_data.get('shutdown_type')
            )
        if filter_form.cleaned_data.get('region'):
            objs = objs.filter(
                region=filter_form.cleaned_data.get('region')
            )
        if filter_form.cleaned_data.get('status'):
            objs = objs.filter(
                status=filter_form.cleaned_data.get('status')
            )
        if filter_form.cleaned_data.get('shutdown_periods_from'):
            objs = objs.filter(
                shutdown_periods_from=filter_form.cleaned_data.get('shutdown_periods_from')
            )
        if filter_form.cleaned_data.get('shutdown_periods_to'):
            objs = objs.filter(
                shutdown_periods_to=filter_form.cleaned_data.get('shutdown_periods_to')
            )
        if filter_form.cleaned_data.get('сause'):
            objs = objs.filter(
                сause=filter_form.cleaned_data.get('сause')
            )
        if filter_form.cleaned_data.get('created_by'):
            objs = objs.filter(
                created_by=filter_form.cleaned_data.get('created_by')
            )
    return render(request, 'dispatching/shutdown_list.html', {'shutdown_list':objs, 'filter_form': filter_form})


def shutdown_delete(request, pk):
    ShutdownLog.objects.get(pk=pk).delete()
    return redirect('apps:dispatching:shutdown_list')


class ShutdownUpdateView(UpdateView):
    """Редактирования отключения"""
    model = ShutdownLog
    context_object_name = 'form'
    template_name = 'dispatching/shutdown_create.html'
    success_url = reverse_lazy('apps:dispatching:shutdown_list')
    fields = ['shutdown_type', 'address','region',
              'status', 'shutdown_periods_from',
              'shutdown_periods_to', 'сause']
