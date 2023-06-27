from django.urls import path
from blog.views import (PageDetailView, PostDetailView, PostListView,
                        AuthorListView, CategoryListView, TagListView,
                        SearchListView)

app_name = 'blog'

urlpatterns = [
  path('', PostListView.as_view(), name='index'),
  path('page/<slug:slug>/', PageDetailView.as_view(), name='page'),
  path('post/<slug:slug>/', PostDetailView.as_view(), name='post'),
  path('author/<int:author_pk>/', AuthorListView.as_view(), name='author'),
  path('category/<slug:slug>/', CategoryListView.as_view(), name='category'),
  path('tag/<slug:slug>/', TagListView.as_view(), name='tag'),
  path('search/', SearchListView.as_view(), name='search'),
]

