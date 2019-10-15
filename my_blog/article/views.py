from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User
#引入markdown
import markdown
#导入数据模型ArticlePost 
from .models import ArticlePost

def article_list(request):
    #取出所有博客文章
    """
    If there is an error occured: ArticlePost do not have objects memerber
    1.pip install pylint-django
    2.in VScode Shift+Ctr+P
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

#文章详情
def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    # 将markdown语法渲染成html
    article.body = markdown.markdown(article.body,
    extensions=[
        # 缩写表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
    ])
    context = {'article': article }
    return render(request, 'article/detail.html', context)


# 写文章的视图
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据但不提交到数据库
            new_article = article_post_form.save(commit=False)
            # 指定id=1的用户为作者
            new_article.author = User.objects.get(id=1)
            # 保存文章到数据库
            new_article.save()
            # 返回文章列表
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新输入。")
    else:
        # 创建表单实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form': article_post_form}
        # 返回模板
        return render(request, 'article/create.html', context)

#删除文章
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        # 调用delte方法
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")
            