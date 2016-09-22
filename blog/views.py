from django.shortcuts import render
from .models import Posts , Comment
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.shortcuts import get_object_or_404
from .forms import EmailForm , CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
# Create your views here.
def home(request, tag_slug=None):
	
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		published = Posts.objects.filter(tags__in=[tag])
	else:
		published = Posts.published.all()
	paginator = Paginator(published,5)
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
	#comments = Comment.objects.filter(post__slug=slug)
	comments = post.comments.filter(active = True)
	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Posts.published.filter(tags__in=post_tags_ids).exclude(slug=post.slug)
	tags = post.tags.all()
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.post = post
			form.save()
	else:
		form = CommentForm()
	return render(request,
		'blog/post/detail.html',
		{'post': post,'comments':comments,'form':form, 'tags':tags, 'similar':similar_posts}
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