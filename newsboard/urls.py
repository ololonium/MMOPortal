from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, CommentCreate, CommentList, CommentDetail, comment_delete, comment_accept
from django.shortcuts import redirect


urlpatterns = [
   path('', PostList.as_view(), name='news'),
   path('<int:pk>', PostDetail.as_view(), name='news-detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('comment/<int:pk>', CommentCreate.as_view(), name='comment_create'),
   path('comments/', CommentList.as_view(), name='comments'),
   path('comments/<int:pk>', CommentDetail.as_view(), name='one_comment'),
   path('comments/<int:pk>/accept/', comment_accept, name='comment_accept'),
   path('comments/<int:pk>/delete/', comment_delete, name='comment_delete'),

]