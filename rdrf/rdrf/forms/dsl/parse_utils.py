from collections import namedtuple
from collections.abc import Iterable
from datetime import datetime
from decimal import Decimal


def is_iterable(el):
    return isinstance(el, Iterable) and not isinstance(el, str)


class SectionHelper:

    def __init__(self, form):
        self.form = form
        self.section_codes = set(s.code for s in self.form.section_models)

    def is_section(self, code):
        return code in self.section_codes

    def get_section_codes(self):
        return self.section_codes

    def get_section_cdes(self, section_code):
        s = [s for s in self.form.section_models if s.code == section_code]
        if s and s[0]:
            return [m.code for m in s[0].cde_models]
        return []

    def get_cde_to_section_dict(self):
        return {
            m.code: (s.code, s.allow_multiple)
            for s in self.form.section_models
            for m in s.cde_models
        }


CDEInfo = namedtuple('CDEInfo', 'name type allow_multiple is_multi_section formset_prefix')


class CDEHelper:

    def __init__(self, form):
        self.cde_names_dict = self.get_cde_names_dict(form)
        self.cde_values_dict = self.get_cde_values_dict(form)

    @staticmethod
    def get_cde_names_dict(form):

        return {
            m.code: (
                CDEInfo(
                    name=f"{s.code}____{m.code}",
                    type=m.widget_name,
                    allow_multiple=m.allow_multiple,
                    is_multi_section=s.allow_multiple,
                    formset_prefix=f"formset_{s.code}" if s.allow_multiple else ''
                )
            )
            for s in form.section_models
            for m in s.cde_models
        }

    @staticmethod
    def get_cde_values_dict(form):
        return {
            m.code: {
                'type': m.datatype,
                'min_value': m.min_value,
                'max_value': m.max_value,
                'max_length': m.max_length,
                'values': {
                    el['value'].lower(): el['code'] for el in m.pv_group.as_dict()['values']
                } if m.pv_group else {},
                'codes': [
                    el['code'] for el in m.pv_group.as_dict()['values']
                ] if m.pv_group else []

            }
            for s in form.section_models
            for m in s.cde_models
        }

    def get_cde_info(self, cde):
        default_info = CDEInfo(cde, None, False, False, '')
        return self.cde_names_dict.get(cde, default_info)

    def get_actual_value(self, cde, value):
        stripped_val = value.strip('"')
        return self.cde_values_dict.get(cde, {}).get('values', {}).get(stripped_val.lower(), stripped_val)

    def is_valid_value(self, cde, value):

        def validate_date(v):
            try:
                datetime.strptime(v, '%d-%m-%Y')
            except ValueError:
                return False
            return True

        def validate_range(v, min_value, max_value):
            try:
                value = Decimal(v)
                is_valid = True
                if min_value:
                    is_valid = value >= min_value
                if max_value:
                    is_valid = valid and value <= max_value
            except ValueError:
                return False
            return is_valid

        stripped_val = value.strip('"')
        values = stripped_val.split(",")
        valid = True
        cde_dict = self.cde_values_dict.get(cde, {})
        values_dict = cde_dict.get('values', {})
        codes_list = cde_dict.get('codes', [])
        if not values_dict:
            if cde_dict.get('type') == 'date':
                return validate_date(stripped_val)
            elif cde_dict.get('min_value') or cde_dict.get('max_value'):
                return validate_range(stripped_val, cde_dict.get('min_value'), cde_dict.get('max_value'))
            elif cde_dict.get('max_length'):
                return len(stripped_val) <= cde_dict.get('max_length')
            else:
                return valid
        else:
            for v in values:
                valid_value = values_dict.get(v.strip().lower()) is not None
                valid_code = v.strip() in codes_list
                valid = valid and (valid_value or valid_code)

        return valid


class EnrichedCDE:

    def __init__(self, cde, cde_helper, has_qualifier=False):
        self.cde = cde
        self.cde_helper = cde_helper
        self.has_qualifier = has_qualifier

    def get_cde_info(self):
        return self.cde_helper.get_cde_info(self.cde)

    def actual_cde_value(self, value):
        parts = value.split(", ")
        if parts and len(parts) > 1:
            values = []
            for part in parts:
                values.append(self.cde_helper.get_actual_value(self.cde, part.strip()))
            return ", ".join(values)
        return self.cde_helper.get_actual_value(self.cde, value)

    def element_name(self):
        return self.cde if self.has_qualifier else self.get_cde_info().name

    def is_multi_section(self):
        return self.get_cde_info().is_multi_section