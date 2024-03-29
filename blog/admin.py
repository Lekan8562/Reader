from django.contrib import admin
from .models import Post,Image,Comment,Tag,Reply,Category,Subsciber

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','publish','status']
    list_filter = ['status','created','publish','author']
    search_fields = ['title','body']
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = 'publish'
    ordering = ['status','publish']

admin.site.register(Image)
admin.site.register(Subsciber)
admin.site.register(Reply)
#admin.site.register(CustomUser)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','post','created','active']
    list_filter = ['active','created','updated']
    search_fields = ['name','email','body']