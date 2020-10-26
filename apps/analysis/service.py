from datetime import datetime

from apps.analysis.models import Punkt5, TotalData, FormAnalysis, Punkt7
from apps.dispatching.models import Event
from apps.opu.objects.models import MainLineType
from django.utils.safestring import mark_safe
from django import template

from apps.dispatching.models import Reason, Index

register = template.Library()
from django.db.models import Q


def division(a: float, b: float) -> float:
    if a != 0 and b != 0:
        return round(a/b, 2)
    return 0


def get_period(obj, date_to):
    if obj.date_to is not None and obj.date_from is not None:
        date = (obj.date_to) - (obj.date_from)
        period_of_time = (((date.total_seconds() / 60) * 100) / 60) / 100
        return period_of_time

    if obj.date_to is None:
        if date_to is not None and date_to != "":
            date_to = datetime.fromisoformat(date_to + "T23:59:59")
            date = date_to - obj.date_from
            period_of_time = (((date.total_seconds() / 60) * 100) / 60) / 100
            return period_of_time
        date = datetime.now()
        newdate = date.replace(hour=23, minute=59, second=59)
        date = newdate - obj.date_from
        period_of_time = (((date.total_seconds() / 60) * 100) / 60) / 100
        return period_of_time


def get_coefficient_kls(downtime):
    if downtime <= 3:
        return 5
    else:
        if downtime > 3:
            if downtime <= 30:
                return 4
            else:
                if downtime > 30:
                    if downtime <= 55:
                        return 3
                    else:
                        if downtime > 55:
                            return 1
                        else:
                            return 0


def get_coefficient_vls(downtime):
    if downtime <= 10:
        return 5
    else:
        if downtime > 10:
            if downtime <= 45:
                return 4
            else:
                if downtime > 45:
                    if downtime <= 85:
                        return 3
                    else:
                        if downtime > 85:
                            return 1
                        else:
                            return 0


def get_coefficient_rrl(downtime):
    if downtime <= 0.5:
        return 5
    else:
        if downtime > 0.5:
            if downtime <= 5:
                return 4
            else:
                if downtime > 5:
                    if downtime <= 30:
                        return 3
                    else:
                        if downtime > 30:
                            return 1
                        else:
                            return 0


def get_type_line(obj) -> int:
    if obj.object is not None:
        return obj.object.type_line.main_line_type.name
    elif obj.circuit is not None:
        return obj.circuit.id_object.type_line.main_line_type.name
    elif obj.ips is not None:
        return obj.ips.object_id.type_line.main_line_type.name


def get_calls_list(all_event, obj):
    if obj.object is not None:
        return all_event.filter(object=obj.object)
    elif obj.ips is not None:
        return all_event.filter(ips=obj.ips)
    elif obj.circuit is not None:
        return all_event.filter(circuit=obj.circuit)


def get_amount_of_channels(obj):
    if obj.object is not None:
        return obj.object.total_amount_active_channels
    elif obj.ips is not None:
        return obj.ips.object_id.total_amount_active_channels
    elif obj.circuit is not None:
        return obj.circuit.id_object.total_amount_active_channels


def get_period_date_to(call, date_to):
    if call.date_to is None:
        date_to = datetime.fromisoformat(date_to + "T23:59:59")
        date = date_to - call.date_from
        period_of_time = (((date.total_seconds() / 60) * 100) / 60) / 100
        return period_of_time
    else:
        return float(call.period_of_time)


def calls_filter_for_punkt5(date_from, date_to, outfit):
    """Фильтрация событии по дате и по предприятию """

    all_event = Event.objects.filter(index1__index='1', callsorevent=False, reason__name=['ПВ аппаратура',
                                                                                          'Линейные ПВ'])


    if outfit is not None:
        all_event = all_event.filter(responsible_outfit_id=outfit)
    if date_from is not None and date_to is None:
        all_event = all_event.filter(created_at=date_from)
    elif date_from is None and date_to is not None:
        all_event = all_event.filter(created_at=date_to)
    elif date_from is not None and date_to is not None:
        all_event = all_event.filter(created_at__gte=date_from, created_at__lte=date_to)

    return all_event


def event_distinct(events, *args):
    """Группировка по филду"""
    return events.order_by(*args).distinct(*args)


def get_type_line_vls_and_kls():
    return MainLineType.objects.get(name__iexact="КЛС"), MainLineType.objects.get(name__iexact="ВЛС")


def create_form_analysis_and_punkt5_punkt7(date_from, date_to, outfit, parent_obj: FormAnalysis, user):
    """Создание п.5"""
    all_event = calls_filter_for_punkt5(date_from, date_to, outfit)
    print(all_event)
    outfits = event_distinct(all_event, "responsible_outfit")
    print(outfits)
    all_event_name = event_distinct(all_event, "ips_id", "object_id", "circuit_id")

    kls, vls = get_type_line_vls_and_kls()

    total_rep_kls = 0
    total_rep_rrl = 0
    for out in outfits:
        reason_1 = 0
        reason_2 = 0
        amount_of_channels = 0
        for event in all_event_name.filter(responsible_outfit=out.responsible_outfit):
            amount_of_channels += int(get_amount_of_channels(event))
            if get_type_line(event) == kls.name:
                reason_1 += get_period_date_to(event, date_to)
            elif get_type_line(event) == vls.name:
                reason_2 += get_period_date_to(event, date_to)

        total_out_kls = reason_1*amount_of_channels
        total_out_rrl = reason_2*amount_of_channels
        total_rep_kls += total_out_kls
        total_rep_rrl += total_out_rrl
        #####################################################################################################
        analysis_form = FormAnalysis.objects.create(outfit=out.responsible_outfit, date_from=date_from,
                                                    date_to=date_to, user=user, id_parent=parent_obj)
        print(analysis_form.outfit.outfit)
        punkt5 = Punkt5.objects.create(outfit_period_of_time_kls=total_out_kls,
                                       outfit_period_of_time_rrl=total_out_rrl, outfit=out.responsible_outfit,
                                       date_from=date_from, date_to=date_to, user=user, form_analysis=analysis_form)
        punkt7 = Punkt7.objects.create(outfit=out.responsible_outfit, date_to=date_to, date_from=date_from,
                                       user=user, form_analysis=analysis_form)
        TotalData.objects.create(punkt5=punkt5)
        TotalData.objects.create(punkt7=punkt7)


    parent_obj.punkt5.outfit_period_of_time_kls += total_rep_kls
    parent_obj.punkt5.outfit_period_of_time_rrl += total_rep_rrl
    parent_obj.punkt5.save()


def get_coefficient_punkt7_kls(percentage_compliance: int) -> int:
    if percentage_compliance < 85:
        return 1
    else:
        if percentage_compliance >= 85:
            if percentage_compliance < 92:
                return 3
            else:
                if percentage_compliance >= 92:
                    if percentage_compliance < 99:
                        return 4
                    else:
                        if percentage_compliance > 99:
                            return 5
                        else:
                            return 0


def get_coefficient_punkt7_rrl(percentage_compliance: int) -> int:
    if percentage_compliance < 85:
        return 1
    else:
        if percentage_compliance >= 85:
            if percentage_compliance < 95:
                return 3
            else:
                if percentage_compliance >= 95:
                    if percentage_compliance < 99:
                        return 4
                    else:
                        if percentage_compliance > 99:
                            return 5
                        else:
                            return 0


def get_coefficient_punkt7_vls(percentage_compliance: int) -> int:
    if percentage_compliance < 84:
        return 1
    else:
        if percentage_compliance >= 84:
            if percentage_compliance < 90:
                return 3
            else:
                if percentage_compliance >= 90:
                    if percentage_compliance < 98:
                        return 4
                    else:
                        if percentage_compliance > 98:
                            return 5
                        else:
                            return 0


def update_downtime(punkt5: Punkt5):
    punkt5.downtime_kls = division(punkt5.outfit_period_of_time_kls, punkt5.length_kls)
    punkt5.downtime_rrl = division(punkt5.outfit_period_of_time_rrl, punkt5.length_rrl)
    punkt5.downtime_vls = division(punkt5.outfit_period_of_time_vls, punkt5.length_vls)
    punkt5.save()


def update_coefficient(punkt5: Punkt5):
    punkt5.coefficient_kls = get_coefficient_kls(punkt5.downtime_kls)
    punkt5.coefficient_rrl = get_coefficient_rrl(punkt5.downtime_rrl)
    punkt5.coefficient_vls = get_coefficient_vls(punkt5.downtime_vls)
    punkt5.save()


def update_total_coefficient(total_data: TotalData):
    punkt5 = total_data.punkt5
    total_data.total_coefficient = division((
            punkt5.coefficient_kls*total_data.kls+punkt5.coefficient_vls*total_data.vls+
            punkt5.coefficient_rrl*total_data.rrl), 100)
    total_data.save()


def update_republic_coefficient(punkt5: Punkt5):
    coefficient = 0
    for form in punkt5.form_analysis.formanalysis_set.all():
        if punkt5.form_analysis.id_parent != form:
            coefficient += form.punkt5.total_data5.total_coefficient
    punkt5.total_data5.total_coefficient = division(coefficient, punkt5.form_analysis.formanalysis_set.count()-1)
    punkt5.total_data5.save()



def update_type_line_value(total_data: TotalData):
    total_data.kls = division(total_data.punkt5.length_kls*100, total_data.total_length)
    total_data.vls = division(total_data.punkt5.length_vls*100, total_data.total_length)
    total_data.rrl = division(total_data.punkt5.length_rrl*100, total_data.total_length)
    total_data.save()


def update_total_length(punkt5: Punkt5):
    punkt5.total_data5.total_length = punkt5.length_vls + punkt5.length_kls + punkt5.length_rrl
    punkt5.total_data5.save()
    update_type_line_value(punkt5.total_data5)


def update_length_and_outfit_period_of_time(form: FormAnalysis):
    outfit_period_of_time_kls = 0
    outfit_period_of_time_rrl = 0
    outfit_period_of_time_vls = 0

    length_kls = 0
    length_rrl = 0
    length_vls = 0

    for analysis_form in form.formanalysis_set.all():
        if analysis_form != form:
            outfit_period_of_time_kls += analysis_form.punkt5.outfit_period_of_time_kls
            outfit_period_of_time_rrl += analysis_form.punkt5.outfit_period_of_time_rrl
            outfit_period_of_time_vls += analysis_form.punkt5.outfit_period_of_time_vls

            length_kls += analysis_form.punkt5.length_kls
            length_rrl += analysis_form.punkt5.length_rrl
            length_vls += analysis_form.punkt5.length_vls

    form.punkt5.outfit_period_of_time_kls = outfit_period_of_time_kls
    form.punkt5.outfit_period_of_time_rrl = outfit_period_of_time_rrl
    form.punkt5.outfit_period_of_time_vls = outfit_period_of_time_vls

    form.punkt5.length_kls = length_kls
    form.punkt5.length_rrl = length_rrl
    form.punkt5.length_vls = length_vls

    form.punkt5.save()


def update_punkt5(punkt5: Punkt5):
    update_downtime(punkt5)
    update_coefficient(punkt5)
    update_total_length(punkt5)
    update_total_coefficient(punkt5.total_data5)

    update_length_and_outfit_period_of_time(punkt5.form_analysis.id_parent)
    update_downtime(punkt5.form_analysis.id_parent.punkt5)
    update_coefficient(punkt5.form_analysis.id_parent.punkt5)
    update_total_length(punkt5.form_analysis.id_parent.punkt5)

    update_republic_coefficient(punkt5.form_analysis.id_parent.punkt5)
    update_analysis_form_coefficient(punkt5.form_analysis.id_parent)


def delete_punkt5(punkt5: Punkt5):
    parent_analysis = punkt5.form_analysis.id_parent
    punkt5_rep = punkt5.form_analysis.id_parent.punkt5
    if punkt5 == punkt5_rep:
        punkt5.form_analysis.delete()
        return
    punkt5.form_analysis.delete()
    update_length_and_outfit_period_of_time(parent_analysis)
    update_downtime(punkt5_rep)
    update_total_length(punkt5_rep)
    update_republic_coefficient(punkt5_rep)

    update_republic_total_number_and_corresponding_norm(parent_analysis)
    update_percentage_compliance_and_coefficient(parent_analysis.punkt7)
    update_total_object(parent_analysis.punkt7)
    update_total_coefficient_punkt7(parent_analysis.punkt7.total_data7)

    update_analysis_form_coefficient(parent_analysis)


def update_analysis_form_coefficient(form_analysis: FormAnalysis):
    form_analysis.coefficient = division(form_analysis.punkt5.total_data5.total_coefficient +
                                         form_analysis.punkt7.total_data7.total_coefficient, 2)
    form_analysis.save()


def update_percentage_compliance(punkt7: Punkt7):
    punkt7.percentage_compliance_kls = division(punkt7.total_number_kls*100, punkt7.corresponding_norm_kls)
    punkt7.percentage_compliance_rrl = division(punkt7.total_number_rrl*100, punkt7.corresponding_norm_rrl)
    punkt7.percentage_compliance_vls = division(punkt7.total_number_vls*100, punkt7.corresponding_norm_vls)
    punkt7.save()


def update_coefficient_punkt7(punkt7: Punkt7):
    punkt7.coefficient_kls = get_coefficient_punkt7_kls(punkt7.percentage_compliance_kls)
    punkt7.coefficient_vls = get_coefficient_punkt7_vls(punkt7.percentage_compliance_vls)
    punkt7.coefficient_rrl = get_coefficient_punkt7_rrl(punkt7.percentage_compliance_rrl)
    punkt7.save()


def update_percentage_compliance_and_coefficient(punkt7: Punkt7):
    update_percentage_compliance(punkt7)
    update_coefficient_punkt7(punkt7)


def update_type_line_value_punkt7(total_data: TotalData):
    total_data.kls = division(total_data.punkt7.total_number_kls*100, total_data.total_length)
    total_data.vls = division(total_data.punkt7.total_number_vls*100, total_data.total_length)
    total_data.rrl = division(total_data.punkt7.total_number_rrl*100, total_data.total_length)
    total_data.save()


def update_total_object(punkt7: Punkt7):
    punkt7.total_data7.total_length = punkt7.total_number_kls+punkt7.total_number_vls+punkt7.total_number_rrl
    punkt7.total_data7.save()
    update_type_line_value_punkt7(punkt7.total_data7)


def update_total_coefficient_punkt7(total_data: TotalData):
    punkt7 = total_data.punkt7
    total_data.total_coefficient = division((
            punkt7.coefficient_kls*total_data.kls+punkt7.coefficient_vls*total_data.vls+
            punkt7.coefficient_rrl*total_data.rrl), 100)
    total_data.save()


def update_republic_total_number_and_corresponding_norm(form: FormAnalysis):
    total_number_kls = 0
    total_number_rrl = 0
    total_number_vls = 0

    corresponding_norm_kls = 0
    corresponding_norm_rrl = 0
    corresponding_norm_vls = 0

    for analysis_form in form.formanalysis_set.all():
        if form != analysis_form:
            total_number_kls += analysis_form.punkt7.total_number_kls
            total_number_vls += analysis_form.punkt7.total_number_vls
            total_number_rrl += analysis_form.punkt7.total_number_rrl

            corresponding_norm_kls += analysis_form.punkt7.corresponding_norm_kls
            corresponding_norm_rrl += analysis_form.punkt7.corresponding_norm_rrl
            corresponding_norm_vls += analysis_form.punkt7.corresponding_norm_vls

    form.punkt7.total_number_kls = total_number_kls
    form.punkt7.total_number_rrl = total_number_rrl
    form.punkt7.total_number_vls = total_number_vls

    form.punkt7.corresponding_norm_kls = corresponding_norm_kls
    form.punkt7.corresponding_norm_rrl = corresponding_norm_rrl
    form.punkt7.corresponding_norm_vls = corresponding_norm_vls

    form.punkt7.save()


def update_punkt7(punkt7: Punkt7):
    update_percentage_compliance_and_coefficient(punkt7)
    update_total_object(punkt7)
    update_total_coefficient_punkt7(punkt7.total_data7)
    update_republic_total_number_and_corresponding_norm(punkt7.form_analysis.id_parent)
    update_percentage_compliance_and_coefficient(punkt7.form_analysis.id_parent.punkt7)
    update_total_object(punkt7.form_analysis.id_parent.punkt7)
    update_total_coefficient_punkt7(punkt7.form_analysis.id_parent.punkt7.total_data7)
    update_analysis_form_coefficient(punkt7.form_analysis)


def delete_punkt7(punkt7: Punkt7):
    rep_punkt7 = punkt7.form_analysis.id_parent.punkt7
    analysis_form = punkt7.form_analysis.id_parent
    if punkt7 == rep_punkt7:
        punkt7.form_analysis.delete()
        punkt7.delete()
        return
    punkt7.form_analysis.delete()
    update_republic_total_number_and_corresponding_norm(analysis_form)
    update_percentage_compliance_and_coefficient(rep_punkt7)
    update_total_object(rep_punkt7)
    update_total_coefficient_punkt7(analysis_form.punkt7.total_data7)

    update_downtime(analysis_form.punkt5)
    update_coefficient(analysis_form.punkt5)
    update_total_length(analysis_form.punkt5)
    update_republic_coefficient(analysis_form.punkt5)

    update_analysis_form_coefficient(analysis_form)

@register.simple_tag
def get_diff(history):
    message = ''
    old_record = history.instance.history_log.filter(Q(history_date__lt=history.history_date)).order_by('history_date').last()
    if history and old_record:
        delta = history.diff_against(old_record)
        for change in delta.changes:
            if "reason" == change.field:
                old_reason = Reason.objects.get(pk=change.old)
                new_reason = Reason.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old_reason, new_reason)
            elif "index1" == change.field:
                old_index = Index.objects.get(pk=change.old)
                new_index = Index.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old_index, new_index)
            else:
                message += "{}:{} ->-> {}".format(change.field, change.old, change.new)
        return mark_safe(message)


