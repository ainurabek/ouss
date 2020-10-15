from datetime import datetime

from apps.analysis.models import Item5, SpecificGravityOfLength, SpecificGravityOfLengthTypeLine, OutfitItem5, \
    FormAnalysis, Item7
from apps.dispatching.models import Event


def division(a: float, b: float) -> float:
    if a != 0 and b != 0:
        return a/b
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


def get_type_line(obj):
    if obj.object is not None:
        return obj.object.type_line.main_line_type.id
    elif obj.circuit is not None:
        return obj.circuit.id_object.type_line.main_line_type.id
    elif obj.ips is not None:
        return obj.ips.object_id.type_line.main_line_type.id


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


def calls_filter_for_item5(date_from, date_to, outfit):
    """Фильтрация событии по дате и по предприятию """
    all_event = Event.objects.filter(index1_id=3, callsorevent=False, reason_id__in=[2, 3])

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


def create_item5(date_from, date_to, outfit, parent_obj):
    """Создание п.5"""
    all_event = calls_filter_for_item5(date_from, date_to, outfit)
    parent_spec = parent_obj.coefficient_item5.total_coefficient
    parent_outfit = parent_obj.coefficient_item5
    parent_spec7 = parent_obj.coefficient_item7.total_coefficient
    parent_outfit7 = parent_obj.coefficient_item7
    outfits = event_distinct(all_event, "responsible_outfit")
    all_event_name = event_distinct(all_event, "ips_id", "object_id", "circuit_id")

    total_rep = 0
    if outfits.count() != 0:
        for out in outfits:
            reason = 0
            amount_of_channels = 0
            for event in all_event_name.filter(responsible_outfit=out.responsible_outfit):
                amount_of_channels += int(get_amount_of_channels(event))

            for call in all_event.filter(responsible_outfit=out.responsible_outfit):
                reason += get_period_date_to(call, date_to)

            total_out = reason*amount_of_channels
            #####################################################################################################
            # create Item5
            space = SpecificGravityOfLength.objects.create(id_parent=parent_spec)
            type_line_value = SpecificGravityOfLengthTypeLine.objects.create(specific_gravity_of_length=space, type_line_id=1)
            out_item = OutfitItem5.objects.create(outfit=out.responsible_outfit, id_parent=parent_outfit,
                                                  total_coefficient=space)
            Item5.objects.create(date_from=date_from, date_to=date_to, type_line_id=1,
                                 outfit_period_of_time=total_out, outfit_item5=out_item,
                                 type_line_value=type_line_value)

            total_rep += total_out
            ############################################################################################################
            # Create Item7
            space7 = SpecificGravityOfLength.objects.create(id_parent=parent_spec7)
            type_line_value = SpecificGravityOfLengthTypeLine.objects.create(
                specific_gravity_of_length=space7, type_line_id=1)
            out_item7 = OutfitItem5.objects.create(outfit=out.responsible_outfit, id_parent=parent_outfit7,
                                                   total_coefficient=space7)
            Item7.objects.create(date_to=date_to, date_from=date_from, type_line_id=1, outfit_item5=out_item7,
                                 type_line_value=type_line_value)

            FormAnalysis.objects.create(id_parent=parent_obj, date_from=date_from,
                                        date_to=date_to, outfit=out.responsible_outfit, coefficient_item5=out_item,
                                        coefficient_item7=out_item7)

            update_form_coefficient(out_item.form_item5)
            update_form_coefficient(out_item7.form_item7)
    else:
        space = SpecificGravityOfLength.objects.create(id_parent=parent_spec)
        type_line_value = SpecificGravityOfLengthTypeLine.objects.create(specific_gravity_of_length=space, type_line_id=1)
        out_item = OutfitItem5.objects.create(outfit=outfit, id_parent=parent_outfit,
                                              total_coefficient=space)
        Item5.objects.create(date_from=date_from, date_to=date_to, type_line_id=1,
                             outfit_period_of_time=0, outfit_item5=out_item, type_line_value=type_line_value)

        ###############################################################################################################
        # Create Item7
        space7 = SpecificGravityOfLength.objects.create(id_parent=parent_spec7)
        type_line_value = SpecificGravityOfLengthTypeLine.objects.create(specific_gravity_of_length=space7, type_line_id=1)
        out_item7 = OutfitItem5.objects.create(outfit=outfit, id_parent=parent_outfit7,
                                               total_coefficient=space7)
        Item7.objects.create(date_to=date_to, date_from=date_from, type_line_id=1, outfit_item5=out_item7,
                             type_line_value=type_line_value)

        FormAnalysis.objects.create(id_parent=parent_obj, date_from=date_from,
                                    date_to=date_to, outfit=outfit, coefficient_item5=out_item,
                                    coefficient_item7=out_item7)
        update_form_coefficient(out_item.form_item5)
        update_form_coefficient(out_item7.form_item7)

    for parent_item5 in parent_outfit.item5.all():
        parent_item5.outfit_period_of_time = total_rep
        parent_item5.save()


def get_coefficient(item5):
    coefficient = 0
    if item5.type_line.name == "КЛС":
        coefficient += get_coefficient_kls(item5.downtime)
    elif item5.type_line.name == "ЦРРЛ":
        coefficient += get_coefficient_rrl(item5.downtime)
    elif item5.type_line.name == "ВОЛС":
        coefficient += get_coefficient_vls(item5.downtime)
    return coefficient


def update_coefficient(item5):
    """Обновление коэффициент качества"""
    coefficient = get_coefficient(item5)
    item5.coefficient = coefficient
    item5.save()


def update_downtime(item5):
    item5.downtime = division(item5.outfit_period_of_time, item5.length)
    item5.save()


def update_downtime_and_coefficient(item5):
    update_downtime(item5)
    update_coefficient(item5)


def update_type_line(out_item5, item7=False):
    if item7:
        for type_line in out_item5.total_coefficient.space.all():
            total_object = 0
            for item in out_item5.item7.filter(type_line=type_line.type_line):
                total_object += item.total_object

            type_line.value = division((total_object * 100), out_item5.total_coefficient.total_length)
            type_line.save()
    else:
        for type_line in out_item5.total_coefficient.space.all():
            length = 0
            for item in out_item5.item5.filter(type_line=type_line.type_line):
                length += item.length

            type_line.value = division((length * 100), out_item5.total_coefficient.total_length)
            type_line.save()


def sum_total_length(out_item5):
    length = 0
    for item5 in out_item5.item5.all():
        length += item5.length
    return length


def sum_total_length_for_item7(out_item5):
    length = 0
    for item7 in out_item5.item7.all():
        length += item7.total_object
    return length


def update_total_length(out_item5):
    out_item5.total_coefficient.total_length = sum_total_length(out_item5)
    out_item5.total_coefficient.save()
    update_type_line(out_item5)


def sum_coefficient(out_item):
    """Суммирование коэффицента"""
    total_coefficient = 0

    for item5 in Item5.objects.filter(outfit_item5=out_item):
        total_coefficient += item5.coefficient
    return total_coefficient


def sum_total_coefficient(out_item5):
    total = 0.0
    for space in out_item5.total_coefficient.specificgravityoflength_set.all():
        total += space.coefficient
    out_item5.total_coefficient.coefficient = division(total, OutfitItem5.objects.filter(id_parent=out_item5).count()-1)
    out_item5.total_coefficient.save()


def update_total_coefficient(out_item, item7=False):
    if item7:
        res = 0
        for type_line in out_item.total_coefficient.space.all():
            for item in out_item.item7.filter(type_line=type_line.type_line):
                res += type_line.value * item.coefficient
        out_item.total_coefficient.coefficient = division(res, 100)
        out_item.total_coefficient.save()
    else:
        res = 0
        for type_line in out_item.total_coefficient.space.all():
            for item in out_item.item5.filter(type_line=type_line.type_line):
                res += type_line.value * item.coefficient
        out_item.total_coefficient.coefficient = division(res, 100)
        out_item.total_coefficient.save()


def update_total_length_and_total_coefficient(out_item):
    update_total_length(out_item)
    update_total_coefficient(out_item)


def create_spec_type_line(out_item5, item5, item7=False):
    """Создание !!!!"""
    if item7:
        type_line = SpecificGravityOfLengthTypeLine.objects.create(type_line=item5.type_line,
                                                       value=division((item5.total_object * 100),
                                                                      out_item5.total_coefficient.total_length),
                                                       specific_gravity_of_length=out_item5.total_coefficient)
        item5.type_line_value = type_line
        item5.save()
    else:
        type_line = SpecificGravityOfLengthTypeLine.objects.create(type_line=item5.type_line,
                                                       value=division(
                                                           (item5.length*100),out_item5.total_coefficient.total_length),
                                                       specific_gravity_of_length=out_item5.total_coefficient)

        item5.type_line_value = type_line
        item5.save()

def check_object(out_item, item5, item7=False):
    if item7:
        if out_item.id_parent.item7.filter(type_line=item5.type_line).exists():
            return True
        return False
    else:
        if out_item.id_parent.item5.filter(type_line=item5.type_line).exists():
            return True
        return False


def get_parent_item5(out_item5, item5, item7=False):
    if item7:
        return out_item5.id_parent.item7.filter(type_line=item5.type_line).get(
            type_line=item5.type_line)
    else:
        return out_item5.id_parent.item5.filter(type_line=item5.type_line).get(type_line=item5.type_line)


def delete_out_item5_and_total(out_item5):
    if out_item5.total_coefficient.space.count() == 0:
        SpecificGravityOfLength.objects.get(pk=out_item5.total_coefficient.id).delete()
        out_item5.delete()



def get_outfit_period_of_time_republic(parent_out_item5, item5, item7=False) -> int:
    rep_outfit_period_of_time = 0
    if item7:
        for out_item in parent_out_item5.parent_out.all():
            if out_item != parent_out_item5:
                for item in out_item.item7.filter(type_line=item5.type_line):
                    rep_outfit_period_of_time += item.total_object
    else:
        for out_item in parent_out_item5.parent_out.all():
            if out_item != parent_out_item5:
                for item in out_item.item5.filter(type_line=item5.type_line):
                    rep_outfit_period_of_time += item.outfit_period_of_time
    return rep_outfit_period_of_time


def update_outfit_period_of_time_republic(parent_out_item5, item5):
    item5.outfit_period_of_time = get_outfit_period_of_time_republic(parent_out_item5, item5)
    item5.save()


def get_republic_length(parent_out_item5, item5, item7=False) -> int:
    rep_length = 0
    if item7:
        for out_item in parent_out_item5.parent_out.all():
            if out_item != parent_out_item5:
                for item in out_item.item7.filter(type_line=item5.type_line):
                    rep_length += item.match_percentage
    else:
        for out_item in parent_out_item5.parent_out.all():
            if out_item != parent_out_item5:
                for item in out_item.item5.filter(type_line=item5.type_line):
                    rep_length += item.length

    return rep_length


def update_length_republic(parent_out_item5, item5):
    item5.length = get_republic_length(parent_out_item5, item5)
    item5.save()


def update_outfit_period_of_time_and_length_republic(parent_out_item5, item5):
    update_outfit_period_of_time_republic(parent_out_item5, item5)
    update_length_republic(parent_out_item5, item5)


def update_item5(new_item5):
    parent_item5 = get_parent_item5(new_item5.outfit_item5, new_item5)
    update_outfit_period_of_time_and_length_republic(new_item5.outfit_item5.id_parent, parent_item5)
    update_downtime_and_coefficient(new_item5)
    update_downtime_and_coefficient(parent_item5)
    update_total_length_and_total_coefficient(new_item5.outfit_item5)
    update_total_length(parent_item5.outfit_item5)
    sum_total_coefficient(parent_item5.outfit_item5)
    update_form_coefficient(parent_item5.outfit_item5.form_item5)
    update_form_coefficient(new_item5.outfit_item5.form_item5)


def item5_delete(item5):
    parent_item5 = get_parent_item5(item5.outfit_item5, item5)
    out_item5 = item5.outfit_item5
    item5.delete()
    update_outfit_period_of_time_and_length_republic(parent_item5.outfit_item5, parent_item5)
    delete_out_item5_and_total(out_item5)
    update_downtime_and_coefficient(parent_item5)
    update_total_length(parent_item5.outfit_item5)
    if str(out_item5) != "None":
        update_total_length_and_total_coefficient(out_item5)
        update_form_coefficient(out_item5.form_item5)
    sum_total_coefficient(parent_item5.outfit_item5)
    update_form_coefficient(parent_item5.outfit_item5.form_item5)


def update_match_percentage(item7):
    item7.match_percentage = division((item7.corresponding_norm*100), item7.total_object)
    item7.save()


def get_coefficient_item7_kls(match_percentage: int) -> int:
    if match_percentage < 85:
        return 1
    else:
        if match_percentage >= 85:
            if match_percentage < 92:
                return 3
            else:
                if match_percentage >= 92:
                    if match_percentage < 99:
                        return 4
                    else:
                        if match_percentage > 99:
                            return 5
                        else:
                            return 0


def get_coefficient_item7_rrl(match_percentage: int) -> int:
    if match_percentage < 85:
        return 1
    else:
        if match_percentage >= 85:
            if match_percentage < 95:
                return 3
            else:
                if match_percentage >= 95:
                    if match_percentage < 99:
                        return 4
                    else:
                        if match_percentage > 99:
                            return 5
                        else:
                            return 0


def get_coefficient_item7_vls(match_percentage: int) -> int:
    if match_percentage < 84:
        return 1
    else:
        if match_percentage >= 84:
            if match_percentage < 90:
                return 3
            else:
                if match_percentage >= 90:
                    if match_percentage < 98:
                        return 4
                    else:
                        if match_percentage > 98:
                            return 5
                        else:
                            return 0


def get_coefficient_item7(item7) -> int:
    coefficient = None
    if item7.type_line.name == "КЛС":
        coefficient = get_coefficient_item7_kls(item7.match_percentage)
    elif item7.type_line.name == "ЦРРЛ":
        coefficient = get_coefficient_item7_rrl(item7.match_percentage)
    elif item7.type_line.name == "ВОЛС":
        coefficient = get_coefficient_item7_vls(item7.match_percentage)
    return coefficient


def update_item7_coefficient(item7):
    item7.coefficient = get_coefficient_item7(item7)
    item7.save()


def update_item7_coefficient_and_match_percentage(item7):
    update_match_percentage(item7)
    update_item7_coefficient(item7)


def update_total_length_item7(out_item):
    out_item.total_coefficient.total_length = sum_total_length_for_item7(out_item)
    out_item.total_coefficient.save()
    update_type_line(out_item, item7=True)


def update_total_coefficient_and_total_length_item7(out_item):
    update_total_length_item7(out_item)
    update_total_coefficient(out_item, item7=True)


def update_total_object(parent_out_item7, item7):
    item7.total_object = get_outfit_period_of_time_republic(parent_out_item7, item7, item7=True)
    item7.save()


def update_corresponding_norm(parent_out_item7, item7):
    item7.corresponding_norm = get_republic_length(parent_out_item7, item7, item7=True)
    item7.save()


def update_total_object_and_corresponding_norm(parent_out_item7, item7):
    update_total_object(parent_out_item7, item7)
    update_corresponding_norm(parent_out_item7, item7)


def update_item7(new_item7):
    update_item7_coefficient_and_match_percentage(new_item7)
    update_total_coefficient_and_total_length_item7(new_item7.outfit_item5)
    parent_item7 = get_parent_item5(new_item7.outfit_item5, new_item7, item7=True)
    update_total_object_and_corresponding_norm(parent_item7.outfit_item5, parent_item7)
    update_item7_coefficient_and_match_percentage(parent_item7)
    update_total_coefficient_and_total_length_item7(parent_item7.outfit_item5)
    update_form_coefficient(parent_item7.outfit_item5.form_item7)
    update_form_coefficient(new_item7.outfit_item5.form_item7)


def item7_delete(item7):
    parent_item7 = get_parent_item5(item7.outfit_item5, item7, item7=True)
    outfit_item7 = item7.outfit_item5
    item7.delete()
    delete_out_item5_and_total(outfit_item7)
    update_total_object_and_corresponding_norm(parent_item7.outfit_item5, parent_item7)
    update_item7_coefficient_and_match_percentage(parent_item7)
    update_total_coefficient_and_total_length_item7(parent_item7.outfit_item5)
    update_form_coefficient(parent_item7.form_item7)
    if str(outfit_item7) != "None":
        update_total_coefficient_and_total_length_item7(outfit_item7)
        update_form_coefficient(outfit_item7.form_item7)


def update_form_coefficient(form_analysis):
    if form_analysis.coefficient_item5 is not None and form_analysis.coefficient_item7 is not None:
        coefficient_item7_and_item5 = form_analysis.coefficient_item5.total_coefficient.coefficient +\
                                      form_analysis.coefficient_item7.total_coefficient.coefficient
        form_analysis.coefficient = division(coefficient_item7_and_item5, 2)
        form_analysis.save()