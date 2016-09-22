from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.


class PostsManager(models.Manager):
	"""docstring for PostsManager"""
	def get_queryset(self):
		return super(PostsManager,self).get_queryset().filter(status='published')


class Posts(models.Model):
	"""docstring for Posts"""
	title = models.CharField(max_length=240)
	body = models.TextField()
	slug = models.SlugField(max_length=250,
		unique_for_date = 'publish',
		blank = True)
	STATUS_CHOICES = (
		('draft', 'Draft'),
		('published', 'Published'),
		)
	publish = models.DateTimeField(default = timezone.now)
	created = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
	status = models.CharField(max_length=10,
		choices = STATUS_CHOICES,
		default = 'draft')
	author = models.ForeignKey(User, related_name = 'blog_posts')
	objects = models.Manager()
	published = PostsManager()
	
	class Meta:
		ordering = ('-publish',)
		verbose_name_plural = 'Posts'

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		from django.core.urlresolvers import reverse
		return reverse('blog:post_detail', args=[str(self.slug)])

	def save(self, *args, **kwargs):
		post_slug = self.title + ' ' + str(self.publish)
		self.slug = slugify(post_slug)
		super(Posts, self).save(*args, **kwargs)

		