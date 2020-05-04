from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from apps.alarm_log.forms import ShutdownFilterForm
from apps.alarm_log.models import Statement, ShutdownLog


class StatementCreateView(CreateView):
    """Создания заявки"""
    model = Statement
    template_name = 'alarm_log/statement_create.html'
    success_url = '/'
    fields = ['type_statement', 'address', 'first_name',
              'type_of_statement', 'status', 'last_name',
              'home_phone', 'telephone_number', 'date_from',
              'date_to', 'specialist', 'description',
              'specialist']

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        return super().form_valid(form)


class ShutdownCreateView(CreateView):
    """Создания отключения"""
    model = ShutdownLog
    fields = ['shutdown_type', 'address','region',
              'status', 'shutdown_periods_from',
              'shutdown_periods_to', 'сause']

    template_name = 'alarm_log/shutdown_create.html'
    success_url = reverse_lazy('apps:alarm_log:shutdown_list')

    def form_valid(self, form):
        print(self.request.user.profile)
        form.instance.created_by = self.request.user.profile
        print(self.request.user.profile)
        return super().form_valid(form)


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
    return render(request, 'alarm_log/shutdown_list.html', {'shutdown_list':objs, 'filter_form': filter_form})


def shutdown_delete(request, pk):
    ShutdownLog.objects.get(pk=pk).delete()
    return redirect('apps:alarm_log:shutdown_list')


class ShutdownUpdateView(UpdateView):
    """Редактирования отключения"""
    model = ShutdownLog
    context_object_name = 'form'
    template_name = 'alarm_log/shutdown_create.html'
    success_url = reverse_lazy('apps:alarm_log:shutdown_list')
    fields = ['shutdown_type', 'address','region',
              'status', 'shutdown_periods_from',
              'shutdown_periods_to', 'сause']
