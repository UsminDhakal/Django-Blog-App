from django.contrib import admin
from .models import BlogPost

# Register your models here.
@admin.register(BlogPost)
class Blogdata(admin.ModelAdmin):
    list_display=['title','desc']