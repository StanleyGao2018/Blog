from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User
#引入markdown
import markdown
from markdown.extensions import Extension
from django.db.models import Q
#导入数据模型ArticlePost 
from .models import ArticlePost, ArticleColumn
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator 
from comment.models import Comment
# 引入评论表单
from comment.forms import CommentForm

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
    # article_list = ArticlePost.objects.all()
    # # 每页先显示一篇文章
    # paginator = Paginator(article_list,3)
    # # 获取url
    # page = request.GET.get('page')
    # # 将导航的对象想相应页码内容返回给article
    # articles = paginator.get_page(page)

    # #需要传递给Template的对象
    # context = {'articles': articles}

    # #render函数： 载入模板 返回context对象
    # return render(request, 'article/list.html', context)

    # 重写articlelist
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    # 初始化查询
    article_list = ArticlePost.objects.all()

    if search:
        # 用Q对象进行联合搜索
        article_list = article_list.filter(
            Q(title__icontains=search)|
            Q(body__icontains=search)
        )
    else :
        search = ''
    # 栏目查询
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)
    # 标签查询
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])
    # 查询排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')
    #     if order == 'total_views':
    #         article_list = ArticlePost.objects.filter(
    #             Q(title__icontains=search) |
    #             Q(body__icontains=search)
    #         ).order_by('-total_views')
    #     else:
    #         article_list = ArticlePost.objects.filter(
    #             Q(title__icontains=search) |
    #             Q(body__icontains=search)
    #         )
    # else:
    #     search = ''
    #     if order == 'total_views':
    #         article_list = ArticlePost.objects.all().order_by('-total_views')
    #     else:
    #         article_list = ArticlePost.objects.all()

    paginator = Paginator(article_list, 7)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 修改此行
    context = { 'articles': articles, 'order': order, 'search': search, 'column': column, 'tag': tag }

    return render(request, 'article/list.html', context)


#文章详情
def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    # 取出评论
    comments = Comment.objects.filter(article=id)
    # 引入频道论表单
    comment_form = CommentForm()
    # 浏览量加一
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # 将markdown语法渲染成html
    md = markdown.Markdown(
    extensions=[
        # 缩写表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        # 目录扩展
        'markdown.extensions.toc',
    ])
    article.body = md.convert(article.body)
    context = { 'article': article, 'toc': md.toc, 'comments': comments, 'comment_form':comment_form }
    return render(request, 'article/detail.html', context)


# 写文章的视图
@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据但不提交到数据库
            new_article = article_post_form.save(commit=False)
            # 指定当前的登录用户为作者
            new_article.author = User.objects.get(id=request.user.id)
            # 将栏目加入
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 保存文章到数据库
            new_article.save()
            # 保存tags多对多的关系
            article_post_form.save_m2m()
            # 返回文章列表
            return redirect("article:article_list")
            
        else:
            return HttpResponse("表单内容有误，请重新输入。")
    else:
        # 创建表单实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {'article_post_form': article_post_form, 'columns': columns}
        # 返回模板
        return render(request, 'article/create.html', context)

#删除文章
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        if request.user !=  article.author:
            return HttpResponse("抱歉，你无法删除这篇文章。")
        # 调用delte方法
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")

# 修改文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章视图函数
    通过post方法提交表单，更新title body
    get方法进入初始表单页面
    id: 文章的id
    """
    article = ArticlePost.objects.get(id=id)

    # 过滤非作者用户
    if request.user != article.author:
        return HttpResponse("sorry, 你无权修改这篇文章。")
    if request.method == "POST":
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断是否满足模型要求
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None

            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            
            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.save()
            # 返回id
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("比但内容有无，请重新填写。")
    
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = { 'article': article, 'article_post_form':article_post_form, 'columns': columns, 'tags': ','.join([x for x in article.tags.names()]) } 
        return render(request, 'article/update.html', context)


