from django.db import models
from utils.rands import slugify_new
from django.contrib.auth.models import User
from utils.resize_image import resize_image
from django_summernote.models import AbstractAttachment
from django.urls import reverse



class PostAttachment(AbstractAttachment):
  def save(self, *args, **kwargs):
    if not self.name:
      self.name = self.file.name

    current_file_name = str(self.file.name)
    super_save = super().save(*args, **kwargs)
    file_changed = False

    if self.file:
      file_changed = current_file_name != self.file.name

    if file_changed:
      resize_image(self.file, 900)

    return super_save


class PublishedManager(models.Manager):
  def get_published(self):
    return self.filter(is_published=True).order_by('-pk')


class Tag(models.Model):
  class Meta:
    verbose_name = "Tag"
    verbose_name_plural = "Tags"

  name = models.CharField(max_length=255)
  slug = models.SlugField(
    unique=True,
    default=None,
    null=True,
    blank=True,
    max_length=100
  )

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify_new(self.name)
    return super().save(*args, **kwargs)

  def __str__(self):
    return self.name


class Category(models.Model):
  class Meta:
    verbose_name = "Category"
    verbose_name_plural = "Categories"

  name = models.CharField(max_length=255)
  slug = models.SlugField(
    unique=True,
    default=None,
    null=True,
    blank=True,
    max_length=100
  )

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify_new(self.name)
    return super().save(*args, **kwargs)

  def __str__(self):
    return self.name


class Page(models.Model):
  title = models.CharField(max_length=255)
  slug = models.SlugField(
    unique=True,
    default=None,
    null=True,
    blank=True,
    max_length=100
  )
  is_published = models.BooleanField(
    default=False,
    help_text='this field needs to be checked for the post to be displayed'
  )
  content = models.TextField()

  objects = PublishedManager()

  def get_absolute_url(self):
    if not self.is_published:
      return reverse('blog:index')
    return reverse('blog:page', args=(self.slug,))

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify_new(self.name)
    return super().save(*args, **kwargs)

  def __str__(self):
    return self.title


class Post(models.Model):
  class Meta:
    verbose_name = "Post"
    verbose_name_plural = "Posts"

  objects = PublishedManager()

  title = models.CharField(max_length=255)
  slug = models.SlugField(
    unique=True,
    default=None,
    null=True,
    blank=True,
    max_length=100
  )
  excerpt = models.CharField(max_length=255)
  is_published = models.BooleanField(
      default=False,
      help_text='this field needs to be checked for the post to be displayed',
    )
  content = models.TextField()
  cover = models.ImageField(
    upload_to='post/%Y/%m/',
    blank=True,
    default=None
  )
  cover_in_post_content = models.BooleanField(
    default=True,
    help_text='Display the cover image inside the post too'
  )
  created_at = models.DateTimeField(auto_now_add=True)
  created_by = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    blank=True,
    null=True,
    # serve para buscar o valor dentro do template ex: user.post_created_by.all
    related_name='post_created_by'
  )
  updated_at = models.DateTimeField(auto_now=True)
  updated_by = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    blank=True,
    null=True,
    related_name='post_updated_by'
  )
  category = models.ForeignKey(
    Category,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    default=None
  )
  tags = models.ManyToManyField(
    Tag,
    blank=True,
    default=''
    )

  def get_absolute_url(self):
    if not self.is_published:
      return reverse('blog:index')
    return reverse('blog:post', args=(self.slug,))


  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify_new(self.name)

    current_cover_name = str(self.cover.name)
    super_save = super().save(*args, **kwargs)
    cover_changed = False

    if self.cover:
      cover_changed = current_cover_name != self.cover.name

    if cover_changed:
      resize_image(self.cover, 900)

    return super_save

  def __str__(self):
    return self.title
