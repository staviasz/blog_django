from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.models import User

from django.views.generic import ListView, DetailView

from blog.models import Post, Page
from utils.erro404 import page404


class PageDetailView(DetailView):
    model = Page
    template_name = "blog/pages/page.html"
    slug_field = "slug"
    context_object_name = "page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f"{page.title} | "

        context.update({"page_title": f"{page_title} - Post | "})
        return context

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/pages/post.html"
    slug_field = "slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        page_title = f"{post.title} | "

        context.update({"page_title": page_title})
        return context

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class PostListView(ListView):
    model = Post
    template_name = "blog/pages/index.html"
    ordering = ("-pk",)
    paginate_by = 6
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "page_title": "Home | ",
            }
        )
        return context


class AuthorListView(PostListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._temp_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self._temp_context["user"]

        user_fullname = user.username
        if user.first_name:
            user_fullname = f"{user.first_name} {user.last_name}"

        page_title = "Posts de " + user_fullname

        context.update(
            {
                "page_title": page_title + " | ",
            }
        )

        return context

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(created_by=self._temp_context["user"].pk)
        return qs

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get("author_pk")
        user = User.objects.filter(pk=author_pk).first()
        page404(user)

        self._temp_context.update(
            {
                "author_pk": author_pk,
                "user": user,
            }
        )

        return super().get(request, *args, **kwargs)


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f"{self.object_list[0].category.name} - Category |"

        context.update(
            {
                "page_title": page_title,
            }
        )

        return context


class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(tags__slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f"{self.object_list[0].tags.first().name} - Tag |"

        context.update(
            {
                "page_title": page_title,
            }
        )

        return context


class SearchListView(PostListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._search_value = ""

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get("search", "").strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        search_value = self._search_value
        return (
            super()
            .get_queryset()
            .filter(
                Q(title__icontains=search_value)
                | Q(excerpt__icontains=search_value)
                | Q(content__icontains=search_value)
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"page_title": "Search | ", "search_value": self._search_value})
        return context

    def get(self, request, *args, **kwargs):
        if self._search_value == "":
            return redirect("blog:index")
        return super().get(request, *args, **kwargs)
