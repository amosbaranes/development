from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.utils.translation import ugettext_lazy as _
from ..courses.models import Course


class PublishedManager(models.Manager): 
    def get_queryset(self): 
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model): 
    STATUS_CHOICES = ( 
        ('draft', 'Draft'), 
        ('published', 'Published'), 
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(_('title'), max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="courses_posts")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    # body = PlaceholderField('post_body')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now) 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='draft')
    
    objects = models.Manager() # The default manager. 
    published = PublishedManager() # Our custom manager.

    tags = TaggableManager(blank=True)

    class Meta: 
        ordering = ('-publish',) 

    def __str__(self): 
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify('post-' + str(self.id) + '-' + self.title)
            super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    comment_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_comments')

    # body = PlaceholderField('comment_body')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 
 
    class Meta: 
        ordering = ('created',) 
 
    def __str__(self): 
        return 'Comment by {} on {}'.format(self.name, self.post)


# https://stackoverflow.com/questions/32625730/how-to-add-a-custom-manager-dynamically-to-model-in-django
# https://scottbarnham.com/blog/2007/04/26/filtering-model-objects-with-a-custom-manager/index.html
# def model_with_queryset(model_class, queryset_class):
#
#     class Proxy(model_class):
#         objects = queryset_class.as_manager()
#
#         class Meta:
#             proxy = True
#             app_label = model_class._meta.app_label
#     return Proxy
#
#
# def get_filter_manager(*args, **kwargs):
#     class FilterManager(models.Manager):
#         """Custom manager filters standard query set with given args."""
#         def get_query_set(self):
#             return super(FilterManager, self).get_query_set().filter(status='published').filter(*args, **kwargs)
#     return FilterManager()
#
#
# def get_post_with_cm(course_id):
#     class FilterManager(models.Manager):
#         """Custom manager filters standard query set with given args."""
#         def get_query_set(self):
#             return super(FilterManager, self).get_query_set().filter(status='published').filter(course__id=course_id)
#
#
#     cm = get_filter_manager(course__id=course_id)
#     post_with_cm = model_with_queryset(Post, cm)
#     return post_with_cm

