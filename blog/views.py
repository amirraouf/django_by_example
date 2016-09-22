from django.shortcuts import render
from .models import Posts
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.shortcuts import get_object_or_404
from .forms import EmailForm
from django.core.mail import send_mail
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

def post_share(request, post_id):
	# Retrieve post by id
	post = get_object_or_404(Posts, id=post_id, status='published')
	sent = False
	if request.method == 'POST':
		# Form was submitted
		form = EmailForm(request.POST)
		if form.is_valid():
			# Form fields passed validation
			cd = form.cleaned_data
			# ... send email
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
			send_mail(subject, message, 'merosr2400@gmail.com',[cd['to']])
			sent = True
	else:
		form = EmailForm()
	return render(request, 'blog/post/share.html', {'post': post,
													'form': form,'sent':sent})