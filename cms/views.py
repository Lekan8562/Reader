from django.shortcuts import render, redirect
from users.models import CustomUser
from blog.models import Subsciber,Post
from django.db.models import Count

# Create your views here.
def home(request):
     if not request.user.is_authenticated:
        return redirect('home') 

    # Assign the authenticated user to the 'author' variable
     author = request.user
     users = CustomUser.objects.count()
     subscribers = Subsciber.objects.count()
     post_count = author.blog_posts.count()
     most_popular_post = author.blog_posts.annotate(total_comments=Count('comments')).order_by('-total_comments')[:1]

    # Your CMS-specific logic here using the 'author' variable
    # For example, retrieve posts authored by the current user
     user_posts = author.blog_posts.all()

     context = {
        'author': author,'user_posts': user_posts,'users':users,'subscribers':subscribers,'most_popular_comment':most_popular_post,'post_count':post_count
     }
     return render(request, 'cms/cms_home.html', context)