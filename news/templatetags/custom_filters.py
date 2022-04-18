from django import template
# import re

register = template.Library()

WORDS_TO_CATCH = [
    'stupid',
    'post1',
    'title',
    'automobile',
]


# Регистрируем наш фильтр под именем censor, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()  # -> {{ text|censor }}
def censor(text_to_check):

    text = text_to_check

    for word in WORDS_TO_CATCH:
        if ((word in text_to_check.lower())
            or ((word + 's') in text_to_check.lower())
            or ((word + 'er') in text_to_check.lower())
            or ((word + 'est') in text_to_check.lower())) \
                and (len(word) > 2):
            substitute = word[0] + '*' * (len(word) - 2) + word[-1]  # about -> a***t
            text = text_to_check.replace(word, substitute)
    return text
    # TODO А если слово в посте с заглавной буквы - оно его не находит
    # TODO Хочу еще регулярками эту х***ю реализовать
    # return ' '.join(word[0] + '*' * (len(word) - 2) + word[-1]
    #                 if (word.strip('.,"?!/-') in WORDS_TO_CATCH) and (len(word) > 2)
    #                 else word
    #                 for word in text_to_check)

