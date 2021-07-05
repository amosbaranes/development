from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from taggit.models import Tag
from .models import Post, Comment
from ..courses.models import Course
from .forms import EmailPostForm, CommentForm, SearchForm, PostForm


def post_list(request, tag_slug=None):
    course_id = request.session.get('course_id')
    course_name = request.session.get('course_name')
    # request.session['course_id'] = course_id
    object_list = Post.published.filter(course__id=course_id).all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag,
                   'course_id': course_id,
                   'course_name': course_name})


def post_create(request):
    course_id = request.session.get('course_id')
    print('===----====')
    print(course_id)
    print('===----====')
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.course = Course.objects.get(id=course_id)
            post.save()
            post_form.save_m2m()
            return redirect('blog:post_list')
    else:
        post_form = PostForm()

    return render(request, 'blog/post/post_create.html', {'post_form': post_form, 'course_id': course_id})


def post_detail(request, year, month, day, post):
    course_id = request.session.get('course_id')
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            new_comment.comment_by = request.user
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(course__id=course_id).filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts
                   , 'course_id': course_id})

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'


def post_share(request, post_id):
    course_id = request.session.get('course_id')
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False 
 
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(request.user.get_full_name(),
                                                                   request.user.email, post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url,
                                                                     request.user.get_full_name(), cd['comments'])
            send_mail(subject, message, request.user.email, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent,
                                                    'course_id': course_id})


def post_search(request):
    course_id = request.session.get('course_id')
    course_name = request.session.get('course_name')
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.filter(course__id=course_id).annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.3).order_by('-similarity')
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results,
                   'course_id': course_id,
                   'course_name': course_name})
