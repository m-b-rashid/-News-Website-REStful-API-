from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, QueryDict
from django.contrib.auth.decorators import login_required

from .models import Comment
from articles.models import Article

#@login_required(login_url='/login/')
def Post(request, id):
    if request.method == "POST":
        if request.user.is_authenticated():
            newComment = request.POST.get('msgbox', None)
            article_instance = Article.objects.get(articleid=id)
            comment_instance = Comment(article=article_instance, user=request.user, comment=newComment)
            if newComment != '':
                comment_instance.save()
                return JsonResponse({'msg': newComment, 'user': comment_instance.user.name})
    else:
        return HttpResponse('Request must be POST.')

def Messages(request, id):
    article_instance = Article.objects.get(articleid=id)
    comment_history = Comment.objects.filter(article=article_instance)
    return render(request, 'messages.html', {'comments': comment_history})

def DeletePost(request):
    if request.method =="DELETE":
        delete = QueryDict(request.body)
        resultID = delete.get('comment_id')
        Comment.objects.filter(pk=resultID).delete()
        return HttpResponse('Success')
    return HttpResponse('Error')
