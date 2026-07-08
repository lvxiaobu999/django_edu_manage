from rest_framework.exceptions import ValidationError


def get_str_param(query_params, name):
    value = query_params.get(name, '')
    return value.strip() if isinstance(value, str) else value


def get_int_param(query_params, name):
    value = get_str_param(query_params, name)
    if value in ('', None):
        return None

    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError({name: f'{name} must be an integer.'}) from exc


def get_choice_param(query_params, name, choices):
    value = get_str_param(query_params, name)
    if not value:
        return ''

    if value not in choices:
        raise ValidationError({name: f'{name} is not a valid choice.'})

    return value
