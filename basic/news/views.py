from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin


# LoginRequiredMixin

from .models import *
from .filters import PostFilter
from .forms import NewsForm, ArtForm
from datetime import datetime
from django.http import HttpResponse


from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect



class PostList(ListView):
   model = Post
   ordering = 'dateCreation'
   template_name = 'posts.html'
   context_object_name = 'posts'
   paginate_by = 10


   # Переопределяем функцию получения списка товаров
   def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = PostFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список товаров
       return self.filterset.qs

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


class PostSearch(ListView):
   model = Post
   ordering = 'dateCreation'
   template_name = 'posts_search.html'
   context_object_name = 'posts'
   paginate_by = 10

   # Переопределяем функцию получения списка товаров
   def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = PostFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список товаров
       return self.filterset.qs

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       return context





# Добавляем новое представление для создания товаров.
class NewsCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)


class ArtCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = ArtForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)


class ArtUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'



class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class ArtDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


# @login_required
# @csrf_protect
# def subscriptions(request):
#     if request.method == 'POST':
#         category_id = request.POST.get('category_id')
#         category = Category.objects.get(id=category_id)
#         action = request.POST.get('action')
#
#         if action == 'subscribe':
#             Subscription.objects.create(user=request.user, category=category)
#         elif action == 'unsubscribe':
#             Subscription.objects.filter(
#                 user=request.user,
#                 category=category,
#             ).delete()
#
#     categories_with_subscriptions = Category.objects.annotate(
#         user_subscribed=Exists(
#             Subscription.objects.filter(
#                 user=request.user,
#                 category=OuterRef('pk'),
#             )
#         )
#     ).order_by('name')
#     return render(
#         request,
#         'subscriptions.html',
#         {'categories': categories_with_subscriptions},
#     )


# class CategoryListView(ListView):
#     model = Post
#     template_name = 'category_list.html'
#     context_object_name = 'category_news_list'
#
#     def get_queryset(self):
#         self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
#         queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dateCreation')
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is not subscriber'] = self.request.user not in self.postCategory.subscribers.all()
#         context['category'] = self.postCategory
#         return context



# @login_required
# def upgrade_me(request):
#     user = request.user
#     premium_group = Group.objects.get(name='author')
#     if not request.user.groups.filter(name='author').exists():
#         premium_group.user_set.add(user)
#     return redirect('/news')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is not subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['category'] = self.postCategory
        return context

@login_required
def subscribe(request, pk):
    user=request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории '
    return render(request, 'subscribe.html', {'category': category, 'message': message})