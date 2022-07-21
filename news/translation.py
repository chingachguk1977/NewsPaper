from .models import Category, Post, Comment, Author

# импортируем декоратор для перевода и класс настроек, от которого наследоваться
from modeltranslation.translator import register, TranslationOptions


# регистрируем модели для перевода

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('cat_name',)  # какие поля надо переводить


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'body',)


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('post', 'body',)
