from datetime import datetime
from apps.analysis.models import Punkt5, TotalData, FormAnalysis, Punkt7
from apps.dispatching.models import Event
from apps.opu.objects.models import MainLineType, Object, IP, Outfit
from django.utils.safestring import mark_safe
from django import template
from apps.dispatching.models import Reason, Index
from django.db.models import Q

register = template.Library()


def division(a: float, b: float) -> float:
    if a != 0 and b != 0:
        return round(a / b, 2)
    return 0


def get_period(obj, date_to):
    if obj.date_to is not None and obj.date_from is not None and date_to is not None:
        if obj.date_to.date() <= datetime.strptime(date_to, '%Y-%m-%d').date():

            return obj.period_of_time

    if date_to is not None:
        date_to = datetime.fromisoformat(date_to + "T23:59:59")
        date = date_to - obj.date_from
        period_of_time = (((date.total_seconds() / 60) * 100) / 60) / 100
        return round(period_of_time, 2)

    date = datetime.now()

    newdate = date.replace(hour=23, minute=59, second=59)

    date = newdate - obj.date_from

    period_of_time = (((date.total_seconds() / 60) * 100) / 60) / 100

    return round(period_of_time, 2)


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



def get_type_line(obj) -> str:

    if obj.object is not None:

        return obj.object.type_line.main_line_type.name

    elif obj.circuit is not None:
        return obj.circuit.id_object.type_line.main_line_type.name



def get_calls_list(all_event, obj):
    if obj.object is not None:
        return all_event.filter(object=obj.object)
    elif obj.ips is not None:
        return all_event.filter(ips=obj.ips)
    elif obj.circuit is not None:
        return all_event.filter(circuit=obj.circuit)


def get_amount_of_channels(obj):
    if obj.object is not None:
        return obj.object.total_amount_channels
    elif obj.circuit is not None:
        return obj.circuit.id_object.total_amount_channels

def get_period_date_to(call, date_to):
    if call.date_to is None:
        date_to = datetime.fromisoformat(date_to + "T23:59:59")
        date = date_to - call.date_from
        period_of_time = (((date.total_seconds() / 60) * 100) / 60) / 100
        return period_of_time
    else:
        return float(call.period_of_time)


def event_filter_date_from_date_to_and_outfit(event: Event, date_from, date_to, outfit) -> Event:

    if not isinstance(outfit, list) and outfit is not None and outfit != '':
        outfit = [outfit]

    if outfit is not None and outfit != '' and outfit != []:
        event = event.filter(responsible_outfit__in=outfit)
    if date_from is not None and date_to is None:
        event = event.filter(Q(date_to__date__gte=date_from) |Q(date_to__date = None))
        event= event.filter(date_from__date__lte=date_from)
    elif date_from is None and date_to is not None:
        event = event.filter(Q(date_to__date__gte=date_to) | Q(date_to__date=None))
        event = event.filter(date_from__date__lte=date_to)
    elif date_from is not None and date_to is not None:
        event = event.filter(Q(date_to__date__gte=date_from) | Q(date_to__date=None), date_from__date__lte=date_to)

    return event


def calls_filter_for_punkt5(date_from, date_to, outfit):
    """Фильтрация событии по дате и по предприятию """

    all_event = Event.objects.filter(index1__index='1', callsorevent=False,
                                     reason__name__in=['ПВ аппаратуры', 'Линейные ПВ', 'Хищения на ЛС']).exclude(name__isnull=False)

    return event_filter_date_from_date_to_and_outfit(all_event, date_from, date_to, outfit)


def event_distinct(events: Event, *args):
    """Группировка по филду"""
    return events.order_by(*args).distinct(*args)


def get_type_line_vls_and_kls():
    return MainLineType.objects.get(name__iexact="КЛС"), MainLineType.objects.get(name__iexact="ЦРРЛ")


def create_form_analysis_and_punkt5_punkt7(date_from, date_to, outfit, punkt7_AK, parent_obj: FormAnalysis, user):
    """Создание п.5"""
    all_event = calls_filter_for_punkt5(date_from, date_to, outfit)
    if outfit:
        outfits = [Outfit.objects.get(pk=outfit), ]
    else:
        outfits = Outfit.objects.filter(outfit__in=['ЧОФ', 'НОФ', 'ТОФ', 'ИОФ', 'ЖОФ', 'ООФ', 'БОФ', 'БГТС', 'ЦСП'])
    all_event_name = event_distinct(all_event, "ips_id", "object_id", "circuit_id")
    kls, rrl = get_type_line_vls_and_kls()
    total_rep_kls = 0
    total_rep_rrl = 0
    for out in outfits:
        total_outfit_kls = 0
        total_outfit_rrl = 0
        for event in all_event_name.filter(responsible_outfit=out):
            total_event_kls = 0
            total_event_rrl = 0
            type_line = get_type_line(event)
            for call in all_event.filter(object=event.object, ips=event.ips, circuit=event.circuit):
                period = get_period(call, date_to)
                if call.ips is None:
                    if type_line == kls.name:
                        total_event_kls += period
                    elif type_line == rrl.name:
                        total_event_rrl += period
                else:
                    if call.ips.total_point_channels_KLS != 0:
                        total_event_kls += period
                    if call.ips.total_point_channels_RRL != 0:
                        total_event_rrl += period
            if event.ips is None:
                amount_of_channels = int(get_amount_of_channels(event))
                if type_line == kls.name:
                    total_outfit_kls += amount_of_channels*total_event_kls
                elif type_line == rrl.name:
                    total_outfit_rrl += amount_of_channels*total_event_rrl
            else:
                if event.ips.total_point_channels_KLS != 0:
                    total_outfit_kls += event.ips.total_point_channels_KLS*total_event_kls
                if event.ips.total_point_channels_RRL != 0:
                    total_outfit_rrl += event.ips.total_point_channels_RRL*total_event_rrl
        total_rep_kls += total_outfit_kls
        total_rep_rrl += total_outfit_rrl
        #####################################################################################################
        analysis_form = FormAnalysis.objects.create(outfit=out, date_from=date_from,
                                                    date_to=date_to, user=user, id_parent=parent_obj)
        if punkt7_AK:
            try:
                form = FormAnalysis.objects.get(outfit=out, id_parent=punkt7_AK)
            except FormAnalysis.DoesNotExist:
                punkt7 = Punkt7.objects.create(outfit=out, date_to=date_to, date_from=date_from,
                                               user=user, form_analysis=analysis_form)
                TotalData.objects.create(punkt7=punkt7)
            else:
                fin_punkt7 = Punkt7.objects.create(form_analysis=analysis_form, user=user,
                                                   outfit=out,
                                                   total_number_kls=form.punkt7.total_number_kls,
                                                   corresponding_norm_kls=form.punkt7.corresponding_norm_kls,
                                                   percentage_compliance_kls=form.punkt7.percentage_compliance_kls,
                                                   coefficient_kls=form.punkt7.coefficient_kls,

                                                   total_number_vls=form.punkt7.total_number_vls,
                                                   corresponding_norm_vls=form.punkt7.corresponding_norm_vls,
                                                   percentage_compliance_vls=form.punkt7.percentage_compliance_vls,
                                                   coefficient_vls=form.punkt7.coefficient_vls,

                                                   total_number_rrl=form.punkt7.total_number_rrl,
                                                   corresponding_norm_rrl=form.punkt7.corresponding_norm_rrl,
                                                   percentage_compliance_rrl=form.punkt7.percentage_compliance_rrl,
                                                   coefficient_rrl=form.punkt7.coefficient_rrl,
                                                   )
                total_data7 = form.punkt7.total_data7
                TotalData.objects.create(punkt7=fin_punkt7, total_length=total_data7.total_length,
                                         total_coefficient=total_data7.total_coefficient, kls=total_data7.kls,
                                         vls=total_data7.vls, rrl=total_data7.rrl)
        else:
            punkt7 = Punkt7.objects.create(outfit=out, date_to=date_to, date_from=date_from,
                                           user=user, form_analysis=analysis_form, total_number_kls=out.total_number_kls,
                                                   corresponding_norm_kls=out.corresponding_norm_kls, total_number_vls=out.total_number_vls,
                                                   corresponding_norm_vls=out.corresponding_norm_vls,  total_number_rrl=out.total_number_rrl,
                                                   corresponding_norm_rrl=out.corresponding_norm_rrl)




            TotalData.objects.create(punkt7=punkt7)
            update_percentage_compliance_and_coefficient(punkt7)
            update_total_object(punkt7)
            update_total_coefficient_punkt7(punkt7.total_data7)
            update_republic_total_number_and_corresponding_norm(punkt7.form_analysis.id_parent)
            update_percentage_compliance_and_coefficient(punkt7.form_analysis.id_parent.punkt7)
            update_total_object(punkt7.form_analysis.id_parent.punkt7)
            update_total_coefficient_punkt7(punkt7.form_analysis.id_parent.punkt7.total_data7)


        punkt5 = Punkt5.objects.create(outfit_period_of_time_kls=round(total_outfit_kls, 2),
                                       outfit_period_of_time_rrl=round(total_outfit_rrl, 2), outfit=out,
                                       length_kls=out.length_kls, length_vls = out.length_vls, length_rrl = out.length_rrl,
                                       date_from=date_from, date_to=date_to, user=user, form_analysis=analysis_form)
        TotalData.objects.create(punkt5=punkt5)
        update_analysis_form_coefficient(punkt7.form_analysis)
        update_analysis_form_coefficient(punkt7.form_analysis.id_parent)
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
            punkt5.coefficient_kls * total_data.kls + punkt5.coefficient_vls * total_data.vls +
            punkt5.coefficient_rrl * total_data.rrl), 100)
    total_data.save()
def update_republic_coefficient(punkt5: Punkt5):
    coefficient = 0
    for form in punkt5.form_analysis.formanalysis_set.all():
        if punkt5.form_analysis.id_parent != form:
            coefficient += form.punkt5.total_data5.total_coefficient
    punkt5.total_data5.total_coefficient = division(coefficient, punkt5.form_analysis.formanalysis_set.count() - 1)
    punkt5.total_data5.save()
def update_type_line_value(total_data: TotalData):
    total_data.kls = division(total_data.punkt5.length_kls * 100, total_data.total_length)
    total_data.vls = division(total_data.punkt5.length_vls * 100, total_data.total_length)
    total_data.rrl = division(total_data.punkt5.length_rrl * 100, total_data.total_length)
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

def update_punkt5(punkt5: Punkt5, total_coefficient: float):
    update_downtime(punkt5)
    update_coefficient(punkt5)
    update_total_length(punkt5)
    if punkt5.formula_activate:
        update_total_coefficient(punkt5.total_data5)
    else:
        punkt5.total_data5.total_coefficient = float(total_coefficient)
        punkt5.total_data5.save()

    update_length_and_outfit_period_of_time(punkt5.form_analysis.id_parent)
    update_downtime(punkt5.form_analysis.id_parent.punkt5)
    update_coefficient(punkt5.form_analysis.id_parent.punkt5)
    update_total_length(punkt5.form_analysis.id_parent.punkt5)

    update_republic_coefficient(punkt5.form_analysis.id_parent.punkt5)
    update_analysis_form_coefficient(punkt5.form_analysis)
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
    punkt7.percentage_compliance_kls = division(punkt7.corresponding_norm_kls, punkt7.total_number_kls) * 100
    punkt7.percentage_compliance_rrl = division(punkt7.corresponding_norm_rrl, punkt7.total_number_rrl) * 100
    punkt7.percentage_compliance_vls = division(punkt7.corresponding_norm_vls, punkt7.total_number_vls) * 100
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
    total_data.kls = division(total_data.punkt7.total_number_kls * 100, total_data.total_length)
    total_data.vls = division(total_data.punkt7.total_number_vls * 100, total_data.total_length)
    total_data.rrl = division(total_data.punkt7.total_number_rrl * 100, total_data.total_length)
    total_data.save()

def update_total_object(punkt7: Punkt7):
    punkt7.total_data7.total_length = punkt7.total_number_kls + punkt7.total_number_vls + punkt7.total_number_rrl
    punkt7.total_data7.save()
    update_type_line_value_punkt7(punkt7.total_data7)

def update_total_coefficient_punkt7(total_data: TotalData):
    punkt7 = total_data.punkt7
    total_data.total_coefficient = division((
            punkt7.coefficient_kls * total_data.kls + punkt7.coefficient_vls * total_data.vls +
            punkt7.coefficient_rrl * total_data.rrl), 100)
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
    update_analysis_form_coefficient(punkt7.form_analysis.id_parent)

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
    old_record = history.instance.history_log.filter(Q(history_date__lt=history.history_date)).order_by(
        'history_date').last()
    if history and old_record:
        delta = history.diff_against(old_record)
        for change in delta.changes:
            if "reason" == change.field:
                old_reason = Reason.objects.get(pk=change.old)
                new_reason = Reason.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old_reason.name, new_reason.name)
            elif "index1" == change.field:
                old_index = Index.objects.get(pk=change.old)
                new_index = Index.objects.get(pk=change.new)
                message += "{}:{} ->-> {}".format(change.field, old_index.index, new_index.index)
            else:
                message += "{}:{} ->-> {}".format(change.field, change.old, change.new)
        return mark_safe(message)


def filter_event(events: Event, instance, index, outfit):

    return events.filter(object=instance.object, ips=instance.ips, circuit=instance.circuit, index1=index, responsible_outfit=outfit)


def get_count_event(events: Event, event, index, outfit) -> int:
    return filter_event(events, event, index, outfit).count()


def get_sum_period_of_time_event(events: Event, instance, index, outfit, date_to):
    a = 0
    for event in filter_event(events, instance, index, outfit):

        a += get_period(event, date_to)

    return a


def determine_the_winner(winners: dict, sum_p: float, winner_index: int) -> dict:
    first = winners["first"]
    second = winners["second"]
    third = winners["third"]

    if sum_p > first["value"]:
        third["value"] = second["value"]
        third["index"] = second["index"]

        second["value"] = first["value"]
        second["index"] = first["index"]

        first["value"] = sum_p
        first["index"] = winner_index

    elif sum_p > second["value"]:

        third["value"] = second["value"]
        third["index"] = second["index"]

        second["value"] = sum_p
        second["index"] = winner_index

    elif sum_p > third["value"]:

        third["value"] = sum_p
        third["index"] = winner_index

    return winners


def set_response_for_winners(winners: dict, index_name: str, data) -> (list, dict):
    first = winners["first"]["index"]
    second = winners["second"]["index"]
    third = winners["third"]["index"]

    if first is not None:
        data[first][index_name]["color"] = True
    if second is not None:
        data[second][index_name]["color"] = True
    if third is not None:
        data[third][index_name]["color"] = True
    winners = {
        "first": {"value": 0, "index": None},
        "second": {"value": 0, "index": None},
        "third": {"value": 0, "index": None}
    }
    return winners


def swap_winners(win1, win2):
    win1["sum"] = win2["sum"]
    win1["name"] = win2["name"]
    win1["count"] = win2["count"]
    return win1, win2


def swap_winners_first_stage(win, name, sum_p, count):
    win["sum"] = sum_p
    win["name"] = name
    win["count"] = count
    return win


def get_winners(winners: list, name, sum_p, count):
    first = winners[0]
    second = winners[1]
    third = winners[2]
    if sum_p > first["sum"]:
        third, second = swap_winners(third, second)
        second, first = swap_winners(second, first)
        first = swap_winners_first_stage(first, name, sum_p, count)

    elif sum_p > second["sum"]:
        third, second = swap_winners(third, second)
        second = swap_winners_first_stage(second, name, sum_p, count)

    elif sum_p > third["sum"]:
        third = swap_winners_first_stage(third, name, sum_p, count)

    return winners


def get_date_to_ak(obj: Event, created_at: str):
    data = obj.date_to
    if obj.date_to is None:
        data = created_at + "T24:00:00"
    elif obj.date_to.date() > datetime.strptime(created_at, '%Y-%m-%d').date():
        data = created_at + "T24:00:00"
    return data

def get_amount(obj:Event):
    if obj.object is not None:
        return obj.object.object_channelKLSRRL.id, obj.object.object_channelKLSRRL.amount_channelsKLS, \
               obj.object.object_channelKLSRRL.amount_channelsRRL
    if obj.ips is not None:
        return  obj.ips.point_channelKLSRRL.id, obj.ips.point_channelKLSRRL.amount_channelsKLS, \
                obj.ips.point_channelKLSRRL.amount_channelsRRL
    if obj.circuit is not None:
        return  None, 1, 1