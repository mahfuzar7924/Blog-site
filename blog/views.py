from django.shortcuts import render,redirect
from blog.models import Post,Category,Comment
from django.db.models import Q
from blog.forms import PostCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def post_list_view(request):
    try:
        query = request.GET.get('query','')
        category_id = request.GET.get('category_id','')
        status = request.GET.get('status','')
        posts = Post.objects.select_related('category','author')

        if category_id:
            posts = posts.filter(category__id = category_id)
        if status:
            posts = posts.filter(status=status)
        if query:
            posts = posts.filter(
                Q(title__icontains = query) |
                Q(content__icontains = query) |
                Q(author__username__icontains =query)
            )

        all_categories = Category.objects.all()
        post_summary_list =[]
        status_choices = Post.STATUS_CHOICES
        for post in posts:
            post_summary_list.append({
                    "id":post.id,
                    "title":post.title,
                    "content":post.content[:100],
                    "category":post.category,
                    "created_at":post.created_at,
                    "last_updated_at":post.updated_at
                }
            )

        return render(
            request=request,
            template_name='post_list.html',
            context={
                'posts':posts,
                'categories':all_categories,
                'post_summary_list':post_summary_list,
                'status_choices':status_choices

            }
        )
     

    except Exception as e:
        return render(
            request=request,
            template_name='error.html',
            context={'error':e}
        )

def post_detail_view(request,pk):
    try:
        post = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post__id=pk)
        parent_comments = post.comments.filter(parent__isnull=True)

        return render(
            request=request,
            template_name='post_detail.html',
            context={
                'comments':comments,
                'parent_comments':parent_comments,
                'post':post,
            }
        )
    except Exception as e:
        return render(
            request=request,
            template_name='error.html',
            context={'error':e}
        )

@login_required
def post_create_view(request):
    try:
        form = PostCreationForm()
        if request.method == "POST":
            form = PostCreationForm(request.POST)
            category_id = request.POST.get('category')
            category = Category.objects.get(id=category_id)
            
            if form.is_valid():
                post = Post(
                    title=request.POST.get('title'),
                    content=request.POST.get('content'),
                    category = category,
                    author = request.user
                )
                post.save()
                return redirect('post_list')

        return render(
            request=request,
            template_name='post_creation.html',
            context={'form':form}
        )

    except Exception as e:
         return render(
            request=request,
            template_name='error.html',
            context={'error':e}
        )