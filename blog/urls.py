from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .feeds import LatestPostsFeed

urlpatterns = [
            path('',views.post_list,name='home'),
            path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/',views.post_detail,name="post_detail"),
            path('post/search/',views.search_posts,name="search"),
            path('<slug:tag_slug>/posts/',views.tag_posts,name='tag_posts'),
            path('posts/<slug:category_slug>/',views.category_posts,name='category_posts'),
            path('comment/<int:post_id>/',views.post_comment,name='post_comment'),
            path('comment/delete/<int:comment_id>/',views.delete_comment,name='delete_comment'),
            path('reply/<int:comment_id>/',views.comment_reply,name='reply'),
            path('post/create/',views.post_create,name="post_create"),
            
            
            path('subscription/user/',views.subscription,name="subscribe"),
            
            path('post/author/<int:author_id>/', views.author_detail,name="author"),
            path('<int:post_id>/share/',views.post_share,name="post_share"),
            
            
            
            path('blog/register/',views.registration_view,name='register'),
            path('user/login/',views.loginPage,name='login'),
            path('user/logout/',views.logoutUser,name='logout'),
            path('feed/',LatestPostsFeed(),name='post_feed'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)