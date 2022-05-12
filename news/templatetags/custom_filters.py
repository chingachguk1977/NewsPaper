from django import template
import re

register = template.Library()

WORDS_TO_CATCH = [
    'stupid',
    'Post2',
    'title',
    'Automobile',
    'about',
    'post1',
    'comment',
    'is',
    'one',
]


# Регистрируем наш фильтр под именем censor, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()  # -> {{ text|censor }}
def censor(text_to_check):
    # Отлавливает стоп-слова в заголовке и тексте поста и заменяет внутренние буквы на звездочки
    # Отлавливает, если на конце стоп-слова в тексте 's', т.е. оно во мн.ч.
    # Игнорирует, соответственно, слова из 1 и 2 букв
    # Игнорирует регистр
    # Игнорирует пунктуацию

    new_text = re.sub(r'[^\w\s]', '', text_to_check)
    word_list = new_text.strip().split()

    # на всякий случай приведем все строки в списке стоп-слов к нижнему регистру,
    # а то вдруг добавим что-то с большой буквы, тогда фильтр не отловит
    new_stop_list = [x.lower() for x in WORDS_TO_CATCH]

    for word in word_list:
        word_len = len(word)
        if (word.lower() in new_stop_list) or (
                (word.lower()[-1] == 's') and (word.lower()[:word_len - 1] in new_stop_list)):
            substitute = word[0] + '*' * (len(word) - 2) + word[-1]  # about -> a***t
            text_to_check = text_to_check.replace(word, substitute)

    return text_to_check

    # если слово в посте с заглавной буквы например - оно его не находит :(
    # text = text_to_check
    #
    # for word in WORDS_TO_CATCH:
    #     if ((word in text_to_check.lower())
    #         or ((word + 's') in text_to_check.lower())
    #         or ((word + 'er') in text_to_check.lower())
    #         or ((word + 'est') in text_to_check.lower())) \
    #             and (len(word) > 2):
    #         substitute = word[0] + '*' * (len(word) - 2) + word[-1]  # about -> a***t
    #         text = text_to_check.replace(word, substitute)
    #
    # return text

    # не отлавливает замену, если до или после слова стоит знак препинания :(
    # return ' '.join(word[0] + '*' * (len(word) - 2) + word[-1]
    #                 if (word.strip('.,"?!/-') in WORDS_TO_CATCH) and (len(word) > 2)
    #                 else word
    #                 for word in text_to_check)
