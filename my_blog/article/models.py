from django.db import models
#导入内建的user模型
from django.contrib.auth.models import User
#timezone 
from django.utils import timezone

# Blog article data models
class ArticlePost(models.Model):
    """文章作者
    argument: on_delete 删除指定数据的方式
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    """文章标题
    models.CharFied 字符串字段，用于保存较短的字符串
    """
    title = models.CharField(max_length=100)

    """
    文章正文 保存大量文本
    """
    body = models.TextField()

    """文章创建时间
    default=timezone.now 指定创建文章是的时间
    """
    created = models.DateTimeField(default=timezone.now)

    """文章更新时间
    auto_now = true 指定每次数据更新时的时间
    """
    update = models.DateTimeField(auto_now=True)

    """
    内部类 class meta 用于给 model 定义元数据
    """
    class Meta:
        #ordering 指定模型返回的数据
        # -created 表明数据应该用倒序排列
        ordering = ('-created',)

    """
    函数 __str__ 定义当调用对象的str() 方法时 返回值
    """
    def __str__(self):
        # 返回标题
        return self.title

