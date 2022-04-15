from django import template

register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()  # (name='currency_rub') -> {{ price|currency_rub }}
def censor(text_to_check):

    return text_to_check
