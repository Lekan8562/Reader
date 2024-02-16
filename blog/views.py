from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from users.models import CustomUser
from django.db.models import Q
from django.conf import settings
from .models import Post,Comment,Tag, Image,Reply, Category
from .forms import CommentForm,PostForm,ReplyForm,RegistrationForm,LoginForm,EmailPostForm,SubsciberForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.utils.text import slugify
from django.core.mail import send_mail
from django.db.models import Count
from PIL import Image as PILImage
from io import BytesIO
import exifread
from django.http import HttpResponseServerError



def search_posts(request):
    query = request.GET.get('q','')
    posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(tag__name__icontains=query)
    ).distinct
    context = {'posts':posts,'query':query}
    return render( request,'blog/post/search.html',context)


def post_share(request,post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"'{post.title}'"
            message = f"Read '{post.title}'' at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comment']}"
            try:
                send_mail(subject, message, 'jegedeolajide2020@gmail.com',[cd['to']])
            except Exception as e:
    # Handle the exception when there's no internet connection
    # You can print an error message or take appropriate action
                print(f"Error sending email: {e}")
                return HttpResponseServerError("Error sending email. Please check your internet connection.")
            sent = True
            
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})
    
def subscription(request):
    if request.method == "POST":
        form = SubsciberForm(request.POST)
        if form.is_valid():
            subscribed = True
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))
    else:
            form = SubsciberForm()
            subscribed = False
    return render(request,'blog/post/home.html',{'form':form,'subscribed':subscribed})
    



def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list,10)
    authors = CustomUser.objects.all()
    categories = Category.objects.all()
    page_number = request.GET.get('page',1)
    latest_posts = Post.published.order_by('publish')[:3]
    popular_posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:3]
    tags = Tag.objects.all()
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'posts':posts,'tags':tags,'latest_posts':latest_posts,'popular_posts':popular_posts,'authors':authors,'categories':categories}
    return render(request,'blog/post/home.html',context)

def post_detail(request,year,month,day,slug):
    posts = Post.published.all()
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED,slug=slug,publish__year=year,publish__month=month,publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    
    post_tags_ids = post.tag.values_list('id',flat=True)
    similar_posts = Post.published.filter(tag__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tag')).order_by('-same_tags','-publish')[:4]
    context = {'post':post,'posts':posts,'comments':comments,'form':form,'similar_posts':similar_posts}
    return render(request,'blog/post/post_detail.html',context)

def tag_posts(request,tag_slug):
    tag = get_object_or_404(Tag,slug=tag_slug)
    tags = Tag.objects.all()
    authors = CustomUser.objects.all()
    latest_posts = Post.published.order_by('publish')[:3]
    context = {'tag':tag,'latest_posts':latest_posts, 'tags':tags,'authors':authors}
    return render(request,'blog/post/tag_posts.html',context)
    
def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    authors = CustomUser.objects.all()
    tags = Tag.objects.all()
    categories = Category.objects.all()
    latest_posts = Post.published.order_by('publish')[:3]
    context = {'category':category,'latest_posts':latest_posts, 'categories':categories,'authors':authors,'tags':tags}
    return render(request,'blog/post/category_posts.html',context)

@require_POST
def post_comment(request,post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return render(request,'blog/post/post_detail.html',{'post':post,'form':form,'comment':comment})


def comment_reply(request,comment_id):
    comment = get_object_or_404(Comment,id=comment_id)
    reply = None
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.save()
            post = comment.post

            # Redirecting to post_detail view using post's attributes
            return redirect('post_detail', year=post.publish.year, month=post.publish.month, day=post.publish.day, slug=post.slug)
        else:
                print(form.errors)
    else:
        form = ReplyForm()
    return render(request,'blog/post/create_reply.html',{'form': form,'comment':comment,'reply':reply})

def delete_comment(request,comment_id):
    comment = get_object_or_404(Comment,id=comment_id)
    comment.delete()
    return redirect(request.META.get('HTTP_REFERER'))

#def loginPage(request):


def post_create(request):
    if request.method == "POST":
         new_title = request.POST.get('title')
         new_body = request.POST.get('body')
         new_status = request.POST.get('status')
         uploaded_images = request.FILES.getlist('images')
         author = request.user
        # if hasattr(current_user,'bloguser'):
        #     blog_user = current_user.bloguser
             
         title_slug = slugify(new_title)
         tag_input = request.POST.get('tag')
         tag_names = [tag.strip() for tag in tag_input.split(',') if tag.strip()]
         post_tags = []
         for tag_name in tag_names:
             tag_slug = slugify(tag_name)
             tag, created = Tag.objects.get_or_create(name=tag_name, defaults={'slug':tag_slug})
             if not created:
                 tag.slug = tag_slug
                 tag.save()
             post_tags.append(tag)
         new_post = Post.objects.create(
                         title = new_title,
                         slug = title_slug,
                         body = new_body,
                         status=new_status,
                         author = author
         )
         new_post.tag.set(post_tags)
         for uploaded_image in uploaded_images: 
             new_image = Image.objects.create(image=uploaded_image)
             new_post.images.add(new_image)
         return redirect('home')
    return render(request,'blog/post/post_create.html')
   
    
    
def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Extract data from the form
            data = form.cleaned_data
            # Create a new CustomUser instance
            new_user = CustomUser.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                username=data['username'],
                email=data['email'],
                avatar=request.FILES.get('avatar'),  # Retrieve uploaded avatar
                bio=data['bio']
                # Add password hashing here if needed
            )
            login(request,new_user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def author_detail(request, author_id):
    author = get_object_or_404(CustomUser, id=author_id)
    context = {'author':author}
    return render(request,'registration/author.html',context)


def loginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticate using email or username along with the password
            user = authenticate(request, username=username_or_email, password=password)
            
            if user is None:
                user = authenticate(request, email=username_or_email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a dashboard or home page
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('home')