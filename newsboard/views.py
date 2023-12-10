from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy, resolve, reverse
from django.http import HttpResponseRedirect, HttpRequest, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .filters import CommentFilter
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from mmoportal import settings


class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'one_news.html'
    context_object_name = 'one_news'


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news')
    permission_required = ('newsboard.add_post', )

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('newsboard.change_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.author == self.request.user:
        #post.author = self.request.user
            return super().form_valid(form)
        else:
            return HttpResponseBadRequest(f'{self.request.user.username}, чтобы редактировать пост, необходимо быть его автором, либо обладать правами администратора.')


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')
    permission_required = ('newsboard.delete_post')


class CommentCreate(PermissionRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comment_edit.html'
    success_url = reverse_lazy('news')
    permission_required = ('newsboard.add_comment')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.comment_author = self.request.user
        comment.comment_post = Post.objects.get(id=self.kwargs.get('pk'))
        comment.save()
        send_mail(subject=f'{comment.comment_post.author}, на Ваше объявление {comment.comment_post.title} оставил отклик {comment.comment_author}.',
                  message=f'{comment.text},'
                          f'Чтобы принять или отклонить перейдите на страницу с откликами на Ваши объявления - {self.request.build_absolute_uri(reverse("comments"))}',
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[comment.comment_post.author.email])
        return redirect(f'/news/{self.kwargs.get("pk")}')




class CommentDetail(PermissionRequiredMixin, DetailView):
    model = Comment
    ordering = '-time_in'
    template_name = 'one_comment.html'
    context_object_name = 'one_comment'
    success_url = reverse_lazy('news')
    permission_required = ('newsboard.add_post')


class CommentList(PermissionRequiredMixin, ListView):
    model = Comment
    ordering = '-time_in'
    template_name = 'comment_list.html'
    context_object_name = 'comments'
    permission_required = ('newsboard.add_post')
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required
def comment_accept(request, **kwargs):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=kwargs.get('pk'))
        comment.active = True
        comment.save()
        send_mail(subject=f'Отклин на объявление {comment.comment_post.title}',
                  message=f'{comment.comment_author},'
                          f'Ваш отклик на объявление {comment.comment_post.title} принят!',
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[comment.comment_author.email])
        return HttpResponseRedirect('/news/comments')
    else:
        return HttpResponseRedirect('/accounts/login')


@login_required
def comment_delete(request, **kwargs):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=kwargs.get('pk'))
        comment.delete()
        send_mail(subject=f'Отклин на объявление {comment.comment_post.title}',
                  message=f'{comment.comment_author},'
                          f'Ваш отклик на объявление {comment.comment_post.title} отклонен!',
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[comment.comment_author.email])
        return HttpResponseRedirect('/news/comments')
    else:
        return HttpResponseRedirect('/accounts/login')