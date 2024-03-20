from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Tag
from .forms import *
from django.contrib import messages
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.
@login_required
def home(request, tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all().order_by('-created')
        
    categories = Tag.objects.all()
    context = {
        'posts':posts,
        'categories':categories,
        'tag' :tag
    }
    return render(request, 'post/index.html', context)

# def category(request, tag):
#     posts = Post.objects.filter(tags__slug=tag)
#     return render(request, 'post/index.html', {'posts':posts})
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            website = requests.get(form.data['url'])
            sourcecode = BeautifulSoup(website.text, 'html.parser')
            
            find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
            image = find_image[0]['content']
            post.image = image 
            
            find_title = sourcecode.select('h1.photo-title')
            title = find_title[0].text.strip()
            post.title = title
            
            find_artist = sourcecode.select('a.owner-name')
            artist = find_artist[0].text.strip()
            post.artist = artist 
            post.author = request.user
            post.save()
            messages.success(request, 'Post Create Successfully')
            return redirect('home')
    else:
        form = PostCreateForm()
    return render(request, 'post/create.html', {'form':form})
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    if request.method=='POST':
        post.delete()
        messages.success(request, 'Post deleted successfully')
        return redirect('home')
    return render(request, 'post/delete.html', {'post':post})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    form = PostEditForm(instance=post)
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post Updated Successfully')
            return redirect('home')
    else:
        form = PostCreateForm(instance=post)
    return render(request, 'post/edit.html', {'post':post,"form":form})

@login_required
def post_page(request, pk):
    post = get_object_or_404(Post, id=pk)
    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()
    categories = Tag.objects.all()
    
    if request.htmx:
        if 'top' in request.GET:
            comments = post.comments.filter(likes__isnull=False)
        else:
            comments = post.comments.all()
        comments = post.comments.all()
        return render(request, 'snippets/loop_postpage_comment.html', {'comments':comments, "categories":categories})
    
    context = {'post':post, 'commentform':commentform, 'replyform':replyform}
    return render(request, 'post/post_page.html', context)

@login_required
def comment_sent(request, pk):
    post = get_object_or_404(Post, id=pk)
    commentform = CommentCreateForm()
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post 
            comment.save()
            
    return render(request, 'snippets/add_comment.html', {'comment':comment, 'commentform':commentform })

@login_required 
def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    replyform = ReplyCreateForm()
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid: 
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()
            
    context = {'comment':comment, 'reply' : reply, "replyform":replyform }
            
    return render(request, 'snippets/add_reply.html', context)

def comment_delete(request, pk):
    post = get_object_or_404(Comment, id=pk, author=request.user)
    if request.method=='POST':
        post.delete()
        return redirect('post_page', post.parent_post)
    return render(request, 'post/comment_delete.html', {'comment':post})

def reply_delete(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)
    if request.method=='POST':
        reply.delete()
        messages.info(request, 'Reply deleted')
        return redirect('post_page', reply.parent_comment.parent_post.id)
    return render(request, 'post/reply_delete.html', {'reply':reply})
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    
    user_exist = post.likes.filter(username=request.user.username).exists()
    
    if post.author != request.user:
        if user_exist:
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        
    return render(request, 'snippets/likes.html', {'post':post})

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    
    user_exist = comment.likes.filter(username=request.user.username).exists()
    
    if comment.author != request.user:
        if user_exist:
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        
    return render(request, 'snippets/likes_comment.html', {'comment':comment})

@login_required
def like_reply(request, pk):
    reply = get_object_or_404(Comment, id=pk)
    
    user_exist = reply.likes.filter(username=request.user.username).exists()
    
    if reply.author != request.user:
        if user_exist:
            reply.likes.remove(request.user)
        else:
            reply.likes.add(request.user)
        
    return render(request, 'snippets/likes_reply.html', {'reply': reply})


      