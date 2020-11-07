from django.shortcuts import render,get_object_or_404
from .models import Post
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.http import HttpResponse
# Create your views here.
from .models import Post, Category, Tag

def tag(request,pk):
    t = get_object_or_404(Tag,pk=pk)
    post_lsit = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request,'blog/index.html', context={'post_list':post_lsit})


def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_lsit = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request,'blog/index.html', context={'post_list':post_lsit})


def archive(request,year,month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})
    # return render(request,'blog/index.html',context={
    #     'title':'我的博客首页',
    #     'welcome':'欢迎访问我的博客首页!'
    # })

def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    md = markdown.Markdown(extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      TocExtension(slugify=slugify),
                                  ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>',md.toc,re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request,'blog/detail.html',context={'post':post})
