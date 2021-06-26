from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Article, Comment
from django.core.paginator import Paginator
from blog.forms import CommentForm


def index(request):
    objs = Article.objects.all()
    paginator = Paginator(objs, 2)
    page_number = request.GET.get('page')
    context = {
        'page_obj': paginator.get_page(page_number),
        'page_number': page_number
    }
    return render(request, 'blog/blog.html', context)


def article(request, pk):
    obj = Article.objects.get(pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = obj
            comment.save()

    comments = Comment.objects.filter(article=obj)
    context = {
        'pk': pk,
        'obj': obj,
        'comments': comments
    }

    # if request.method == 'POST':
    #     comment = request.POST.get('comment')
    #     context['text'] = comment

    return render(request, 'blog/article.html', context)
