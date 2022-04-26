from django_filters import FilterSet, ModelMultipleChoiceFilter, ModelChoiceFilter
from .models import Post, Category, Author


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    category = ModelMultipleChoiceFilter(
        field_name='postcategory__cat_thru',
        queryset=Category.objects.all(),
        label='Category',
        #empty_label='Any',  # нужно, только если ModelChoiceFilter, а не ModelMultipleChoiceFilter
        conjoined=True,  # нужно, только если ModelMultipleChoiceFilter, а не ModelChoiceFilter
                           # также нужно, если множественный фильтр работал по AND, а не по OR
    )

    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Author',
        empty_label='Any',  # нужно, только если ModelChoiceFilter, а не ModelMultipleChoiceFilter
        #conjoined=True,  # нужно, только если ModelMultipleChoiceFilter, а не ModelChoiceFilter
                           # также нужно, если множественный фильтр работал по AND, а не по OR
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'title': ['icontains'],
            'author': ['exact'],
            'rating': [
                'lt',  # рейтинг должна быть меньше или равна указанной
                'gt',  # рейтинг должна быть больше или равна указанной
            ],
        }