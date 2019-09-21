from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from .views import ReplyCreateView, ReplyUpdateView, ReplyDeleteView

urlpatterns = [
    # path('', views.home, name='forum-home'),
    path('', PostListView.as_view(), name='forum-home'),
    path('devlog/', views.devlog, name="forum-devlog"),
    path('about/', views.about, name='forum-about'),
    path('back/<int:post_pk>', views.back, name='back'),

    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),

    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),

    path('reply/<int:pk>/new', ReplyCreateView.as_view(), name='reply-create'),
    path('reply/<int:pk>/update', ReplyUpdateView.as_view(), name='reply-update'),
    path('reply/<int:pk>/delete', ReplyDeleteView.as_view(), name='reply-delete'),
]