from django.urls import path
# Импортируем созданное нами представление
from .views import (
   PostsList,
   PostDetail,
   PostCreate,
   CategoryDetail,
   create_post,
   PostUpdate,
   PostDelete,
   PostSearchView,
   PostAuthor,
   subscribe_to_category,
   unsubscribe_from_category,
   PostType,
   PostTag, subscribe_to_author, unsubscribe_from_author
)

app_name = 'news'
urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   # path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
   # path('create/', create_post, name='post_create'),
   path('create/', PostCreate.as_view(), name='post_create'),
   # path('add/', PostCreate.as_view(), name='post_create'),
   # path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search/', PostSearchView.as_view(), name='post_search'),
   path('author/<int:pk>', PostAuthor.as_view(), name='author_name'),
   path('subscribe/category/<int:pk>', subscribe_to_category, name='sub_cat'),
   path('unsubscribe/category/<int:pk>', unsubscribe_from_category, name='unsub_cat'),
   path('subscribe/author/<int:pk>', subscribe_to_author, name='sub_author'),
   path('unsubscribe/author/<int:pk>', unsubscribe_from_author, name='unsub_author'),
   path('tag/<int:pk>', PostTag.as_view(), name='post_tag'),
   path('type/<str:title>', PostType.as_view(), name='post_type'),
   # path('profile_update/', ProfileUpdate.as_view(), name='profile_update'),
   # path('accounts/profile/', ProfileUpdate.as_view(), name='profile_update'),
]
