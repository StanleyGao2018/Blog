from django.shortcuts import render
#导入数据模型ArticlePost 
from .models import ArticlePost

def article_list(request):
    #取出所有博客文章
    """
    If there is an error occured: ArticlePost do not have objects memerber
    1.pip install pylint-django
    2.in VScode Shift+Command+P
    3.Type into Preferences: Configure Language Specific Settings. Now select Python
    4.Add following code 
        {"python.linting.pylintArgs": [
            "--load-plugins=pylint_django"
        ],}
    """
    articles = ArticlePost.objects.all()

    #需要传递给Template的对象
    context = {'articles': articles}

    #render函数： 载入模板 返回context对象
    return render(request, 'article/list.html', context)

