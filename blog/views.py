from django.shortcuts import render
from .models import Posts
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.shortcuts import get_object_or_404
# Create your views here.
def home(request):
	published = Posts.published.all()
	paginator = Paginator(published,3)
	page = request.GET.get('page')
	try:
		published = paginator.page(page)
	except PageNotAnInteger:
		published = paginator.page(1)
	except EmptyPage:
		published = paginator.page(paginator.num_pages)
	context = {'posts': published,
	'page':page,
	}
	return render(request, 'blog/post/home.html', context)

def post_detail(request,slug):

	post = get_object_or_404(Posts,slug = slug)
	print "post.slug"
	return render(request,
		'blog/post/detail.html',
		{'post': post}
		)

#This is home view as class based
# from django.views.generic import ListView


# class Home(ListView):
# 	queryset = Post.published.all()
# 	context_object_name = 'posts'
# 	paginate_by = 3
# 	template_name = 'blog/post/list.html'