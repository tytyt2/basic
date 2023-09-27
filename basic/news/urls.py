from django.urls import path
# Импортируем созданное нами представление
from .views import PostDetail, PostList, PostSearch, NewsCreate, ArtCreate , NewsUpdate, ArtUpdate, \
   NewsDelete, ArtDelete, CategoryListView, subscribe #subscriptions


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search', PostSearch.as_view(), name='post_search'),


   path('news/create', NewsCreate.as_view(), name='post_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

   path('articles/create', ArtCreate.as_view(), name='post_create'),
   path('articles/<int:pk>/edit/', ArtUpdate.as_view(), name='art_update'),
   path('articles/<int:pk>/delete/', NewsDelete.as_view(), name='art_delete'),


   # path('subscriptions/', subscriptions, name='subscriptions'),
   path('categories/<int:pk>', CategoryListView.as_view(), name = 'category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),


]