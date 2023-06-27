from django.urls import path
from blog.views import index, page, post, author, category, tag

app_name = 'blog'

urlpatterns = [
  path('', index, name='index'),
  path('page/<slug:slug>/', page, name='page'),
  path('post/<slug:slug>/', post, name='post'),
  path('author/<int:author_pk>/', author, name='author'),
  path('category/<slug:slug>/', category, name='category'),
  path('tag/<slug:slug>/', tag, name='tag'),
]

