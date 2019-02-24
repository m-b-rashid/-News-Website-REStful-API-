from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from urllib import parse

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import RedirectView
from .forms import ArticleForm
from .models import Article
from django.db.models import Count

from comments.models import Comment
# Create your views here.


def article_list(request):
	#seperates all articles into pages using paginator
    queryset = Article.objects.all()
    paginator = Paginator(queryset, 5)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        querysubset = paginator.page(page)
    except PageNotAnInteger:
        querysubset = paginator.page(1)
    except EmptyPage:
        querysubset = paginator.page(paginator.num_pages)
    context = { "object_list" : querysubset, "title" : "List", "page_request_var" : page_request_var}
    return render(request, "article_list.html", context)

def article_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Article has been created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "ERROR: Article has NOT been created")
    context = {"form" : form}
    return render(request, "article_form.html", context)

@ensure_csrf_cookie
def article_detail(request, id):
    instance = get_object_or_404(Article, articleid=id)
    comment_instance = Comment.objects.filter(article=id)
    share_string = parse.quote_plus(instance.title)
    context = { "title" : "Detail", "instance" : instance, "share_string" : share_string,  "comments" : comment_instance, }
    return render(request, "article_detail.html", context)

def article_update(request, id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Article, articleid=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Article has been updated")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = { "title" : "Detail", "instance" : instance, "form" : form}
    return render(request, "article_form.html", context)

def article_delete(request, id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Article, articleid=id)
    instance.delete()
    messages.success(request, "Article has been deleted succesfully")
    return redirect("articles:list")

def article_filter(request):
    if request.method == "GET":
        genre = request.GET.get('genre')
        if(genre == 'ALL'):
            queryset = Article.objects.all()
        else:
            queryset = Article.objects.filter(genre=genre)
        paginator = Paginator(queryset, 5)
        page = request.GET.get("page")
        try:
            querysubset = paginator.page(page)
        except PageNotAnInteger:
            querysubset = paginator.page(1)
        except EmptyPage:
            querysubset = paginator.page(paginator.num_pages)
    json_result = serializers.serialize('json', querysubset)
    return JsonResponse(json_result, DjangoJSONEncoder, False)

def yolo(request):
	#nightlystormers-easteregg
    return render(request, "yolo.html", {})

def article_like(request, id):
    obj = get_object_or_404(Article, articleid=id)
    user = request.user
    if user.is_authenticated():
        removeLike = False
        addLike = False
        removeDislike = False
        if user in obj.likes.all():
            obj.likes.remove(user)
            removeLike = True
        else:
            obj.likes.add(user)
            addLike = True
            if user in obj.dislikes.all():
                obj.dislikes.remove(user)
                removeDislike = True
    number = obj.likes.count()
    dislike = obj.dislikes.count()
    print (number)
    data = {
    "dislikeNo": dislike,
    "likeNo": number,
    "removeLike": removeLike,
    "addLike": addLike,
    "removeDislike": removeDislike
    }
    return JsonResponse(data, DjangoJSONEncoder, False)

def article_dislike(request, id):
    obj = get_object_or_404(Article, articleid=id)
    user = request.user
    removeDislike = False
    addDislike = False
    removeLike = False
    if user.is_authenticated():
        if user in obj.dislikes.all():
            obj.dislikes.remove(user)
            removeDislike = True
        else:
            obj.dislikes.add(user)
            addDislike = True
            if user in obj.likes.all():
                obj.likes.remove(user)
                removeLike = True
    number = obj.likes.count()
    dislike = obj.dislikes.count()
    data = {
    "dislikeNo": dislike,
    "likeNo": number,
    "removeDislike":removeDislike,
    "addDislike":addDislike,
    "removeLike":removeLike
    }
    return JsonResponse(data, DjangoJSONEncoder, False)
