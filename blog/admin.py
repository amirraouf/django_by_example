from django.contrib import admin
from .models import Posts
# Register your models here.
class PostAdmin(admin.ModelAdmin):
	list_filter = ('publish', 'status')
	search_fields = ('title', 'body')
admin.site.register(Posts, PostAdmin)