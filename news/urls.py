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
)


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   # path('create/', create_post, name='post_create'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search/', PostSearchView.as_view(), name='post_search'),
   # path('profile_update/', ProfileUpdate.as_view(), name='profile_update'),
   # path('accounts/profile/', ProfileUpdate.as_view(), name='profile_update'),
]
